#!/usr/bin/env python3
"""Standard-library algebra checks; no training or experimental performance claims."""
import json
import math
from pathlib import Path
import random

SEED = 20261023
DRAWS = 200_000

def forces(g, b, a, u):
    left = (g + b) * (a + u)
    right = (g - b) * (a - u)
    return left, right, left + right, left - right

def close(x, y):
    return math.isclose(x, y, rel_tol=1e-11, abs_tol=1e-11)

def main():
    rng = random.Random(SEED)
    algebra_checks = 0
    for _ in range(1000):
        g = rng.uniform(0.6, 2.0)
        b = rng.uniform(-0.8*g, 0.8*g)
        a = rng.uniform(0.5, 1.0)
        u = rng.uniform(-a, a)
        delta = rng.uniform(0.01, a)
        left, right, total, diff = forces(g,b,a,u)
        assert close(total, 2*g*a+2*b*u)
        assert close(diff, 2*b*a+2*g*u)
        ml, mr, mt, md = forces(g,-b,a,-u)
        assert close(ml,right) and close(mr,left)
        assert close(mt,total) and close(md,-diff)
        plus, minus = forces(g,b,a,delta), forces(g,b,a,-delta)
        slope_even = (plus[2]-minus[2])/(2*delta)
        slope_odd = (plus[3]-minus[3])/(2*delta)
        reflected_plus, reflected_minus = forces(g,-b,a,delta), forces(g,-b,a,-delta)
        reflected_even = (reflected_plus[2]-reflected_minus[2])/(2*delta)
        reflected_odd = (reflected_plus[3]-reflected_minus[3])/(2*delta)
        assert close(slope_even,2*b) and close(reflected_even,-slope_even)
        assert close(slope_odd,2*g) and close(reflected_odd,slope_odd)
        e_left,e_right = rng.uniform(-5,5),rng.uniform(-5,5)
        assert close((e_left+e_right)**2+(e_left-e_right)**2,2*(e_left**2+e_right**2))
        even, odd_1, odd_2 = g,b,u
        assert close(even*(-odd_1),-(even*odd_1))
        assert close((-odd_1)*(-odd_2),odd_1*odd_2)
        # SAME anatomical query u for b and -b: no reflection of query here.
        mean_plus = forces(g,b,a,u)[2]
        mean_minus = forces(g,-b,a,u)[2]
        midpoint = (mean_plus+mean_minus)/2
        bound = (mean_plus-mean_minus)**2/4
        risk = lambda c: ((mean_plus-c)**2+(mean_minus-c)**2)/2
        assert close(risk(midpoint),bound)
        for displacement in [-2,-0.25,0.25,2]:
            assert close(risk(midpoint+displacement),bound+displacement**2)
        assert close(bound,4*b*b*u*u)
        # Independent zero-mean outcome noise adds variance to both Bayes risks,
        # leaving the excess caused by collapsed memory equal to the bound.
        noise_variance = 0.4
        assert close((bound+noise_variance)-noise_variance,bound)
        algebra_checks += 1
    # Independent RK4 integration of actuator activation and accumulated force.
    # This checks the finite-horizon formula in the final proposal, not a trained model.
    impulse_max_error = 0.0
    impulse_cases = 0
    for gain in (0.8, 1.0, 1.2):
        for imbalance in (-0.2, 0.2):
            for lag in (0.05, 0.15):
                common, query, horizon, step = 0.6, 0.25, 0.5, 0.001
                state = (common, common, 0.0)
                def deriv(z):
                    q_left, q_right, _ = z
                    return ((common + query - q_left)/lag,
                            (common - query - q_right)/lag,
                            (gain + imbalance)*q_left + (gain - imbalance)*q_right)
                for _ in range(round(horizon/step)):
                    k1 = deriv(state)
                    k2 = deriv(tuple(x + step*d/2 for x,d in zip(state,k1)))
                    k3 = deriv(tuple(x + step*d/2 for x,d in zip(state,k2)))
                    k4 = deriv(tuple(x + step*d for x,d in zip(state,k3)))
                    state = tuple(x + step*(a+2*b+2*c+d)/6
                                  for x,a,b,c,d in zip(state,k1,k2,k3,k4))
                expected = 2*gain*common*horizon + 2*imbalance*query*(
                    horizon-lag*(1-math.exp(-horizon/lag)))
                error = abs(state[2]-expected)
                assert error < 1e-9
                impulse_max_error = max(impulse_max_error,error)
                impulse_cases += 1
    b0,delta,sigma = 0.2,0.25,0.12
    analytical = 0.5*math.erfc((2*math.sqrt(2)*b0*delta/sigma)/math.sqrt(2))
    noise_rng = random.Random(SEED)
    errors = 0
    for _ in range(DRAWS):
        sign = 1 if noise_rng.random() < 0.5 else -1
        difference = 4*sign*b0*delta + noise_rng.gauss(0,sigma) - noise_rng.gauss(0,sigma)
        errors += sign*difference < 0
    empirical = errors/DRAWS
    standard_error = math.sqrt(analytical*(1-analytical)/DRAWS)
    assert abs(empirical-analytical) < 5*standard_error
    result = {
        'status':'passed', 'scope':'algebra, numerical integration, and a toy Gaussian Monte Carlo check only; no trained models',
        'random_seed':SEED, 'randomized_algebra_cases':algebra_checks,
        'checks':['bilateral force identities','joint body/action reflection','finite-slope parity',
                  'sum/difference squared-error identity','even/odd product rules',
                  'same-query collapsed-memory excess MSE','Gaussian sign-error Monte Carlo',
                  'finite-horizon impulse versus independent RK4 integration'],
        'dynamic_impulse_check':{'cases':impulse_cases,'max_absolute_error_N_s':impulse_max_error,
            'integration_step_seconds':0.001,'horizon_seconds':0.5},
        'gaussian_sign_error':{'draws':DRAWS,'b0':b0,'delta':delta,'sigma':sigma,
            'analytic_probability':analytical,'monte_carlo_probability':empirical,
            'binomial_standard_error_under_analytic_model':standard_error,
            'difference_in_standard_errors':(empirical-analytical)/standard_error},
        'collapse_bound':{'assumptions':['two histories conditionally equally likely at the merged memory and fixed query','identical retained memory',
            'same future query for both histories','squared-error loss','conditional outcome means m_plus and m_minus'],
            'minimal_excess_mse':'(m_plus - m_minus)^2 / 4',
            'toy_total_force_specialization':'4*b^2*u^2',
            'qualification':'An elementary diagnostic identity. It neither proves learned-memory collapse nor applies to reflected queries as if they were identical.'}
    }
    out = Path(__file__).with_name('analytic-check-results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
