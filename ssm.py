import numpy as np


class LinearStateSpaceModel:
    """A small linear Gaussian state space model implemented with NumPy.

    The model is defined by the equations

        x_t = A x_{t-1} + w_t,   w_t ~ N(0, Q)
        y_t = C x_t     + v_t,   v_t ~ N(0, R)

    where x_t is the latent state and y_t is the observation.
    """

    def __init__(self, transition, observation, process_cov, observation_cov, initial_mean, initial_cov):
        self.A = np.asarray(transition, dtype=float)
        self.C = np.asarray(observation, dtype=float)
        self.Q = np.asarray(process_cov, dtype=float)
        self.R = np.asarray(observation_cov, dtype=float)
        self.x0 = self._as_vector(initial_mean)
        self.P0 = np.asarray(initial_cov, dtype=float)

        self._validate_shapes()

    @property
    def state_dim(self):
        return self.A.shape[0]

    @property
    def obs_dim(self):
        return self.C.shape[0]

    def step(self, state, rng=None):
        """Advance the latent state by one time step."""
        rng = np.random.default_rng() if rng is None else rng
        state = self._as_vector(state)
        noise = rng.multivariate_normal(np.zeros(self.state_dim), self.Q)
        return self.A @ state + noise

    def observe(self, state, rng=None):
        """Generate an observation from a latent state."""
        rng = np.random.default_rng() if rng is None else rng
        state = self._as_vector(state)
        noise = rng.multivariate_normal(np.zeros(self.obs_dim), self.R)
        return self.C @ state + noise

    def simulate(self, num_steps, rng=None):
        """Simulate latent states and observations.

        Returns a tuple (states, observations) with shapes
        (num_steps, state_dim) and (num_steps, obs_dim).
        """
        if num_steps <= 0:
            raise ValueError("num_steps must be positive")

        rng = np.random.default_rng() if rng is None else rng
        states = np.zeros((num_steps, self.state_dim), dtype=float)
        observations = np.zeros((num_steps, self.obs_dim), dtype=float)

        state = rng.multivariate_normal(self.x0, self.P0)
        for index in range(num_steps):
            state = self.step(state, rng=rng)
            observation = self.observe(state, rng=rng)
            states[index] = state
            observations[index] = observation

        return states, observations

    def kalman_filter(self, observations):
        """Run Kalman filtering over a sequence of observations.

        Returns a dictionary containing predicted and filtered means and
        covariances, along with innovations and log-likelihood.
        """
        observations = np.asarray(observations, dtype=float)
        if observations.ndim == 1:
            observations = observations[:, np.newaxis]
        if observations.shape[1] != self.obs_dim:
            raise ValueError("observations must have shape (n_steps, obs_dim)")

        num_steps = observations.shape[0]
        predicted_means = np.zeros((num_steps, self.state_dim), dtype=float)
        predicted_covs = np.zeros((num_steps, self.state_dim, self.state_dim), dtype=float)
        filtered_means = np.zeros((num_steps, self.state_dim), dtype=float)
        filtered_covs = np.zeros((num_steps, self.state_dim, self.state_dim), dtype=float)
        innovations = np.zeros((num_steps, self.obs_dim), dtype=float)
        log_likelihood = 0.0

        mean = self.x0.copy()
        covariance = self.P0.copy()

        identity = np.eye(self.state_dim)

        for index, observation in enumerate(observations):
            pred_mean = self.A @ mean
            pred_cov = self.A @ covariance @ self.A.T + self.Q

            innovation = observation - self.C @ pred_mean
            innovation_cov = self.C @ pred_cov @ self.C.T + self.R
            gain = pred_cov @ self.C.T @ np.linalg.inv(innovation_cov)

            mean = pred_mean + gain @ innovation
            covariance = (identity - gain @ self.C) @ pred_cov

            predicted_means[index] = pred_mean
            predicted_covs[index] = pred_cov
            filtered_means[index] = mean
            filtered_covs[index] = covariance
            innovations[index] = innovation
            log_likelihood += self._gaussian_logpdf(innovation, innovation_cov)

        return {
            "predicted_means": predicted_means,
            "predicted_covs": predicted_covs,
            "filtered_means": filtered_means,
            "filtered_covs": filtered_covs,
            "innovations": innovations,
            "log_likelihood": float(log_likelihood),
        }

    def _validate_shapes(self):
        if self.A.ndim != 2 or self.A.shape[0] != self.A.shape[1]:
            raise ValueError("transition must be a square 2D matrix")
        if self.C.ndim != 2 or self.C.shape[1] != self.A.shape[0]:
            raise ValueError("observation must have shape (obs_dim, state_dim)")
        if self.Q.shape != self.A.shape:
            raise ValueError("process_cov must match transition shape")
        if self.R.ndim != 2 or self.R.shape[0] != self.R.shape[1]:
            raise ValueError("observation_cov must be a square 2D matrix")
        if self.R.shape[0] != self.C.shape[0]:
            raise ValueError("observation_cov must match observation dimension")
        if self.x0.shape != (self.A.shape[0],):
            raise ValueError("initial_mean must have shape (state_dim,)")
        if self.P0.shape != self.A.shape:
            raise ValueError("initial_cov must match transition shape")

    @staticmethod
    def _as_vector(value):
        array = np.asarray(value, dtype=float)
        if array.ndim == 2 and 1 in array.shape:
            return array.reshape(-1)
        if array.ndim != 1:
            raise ValueError("expected a 1D vector")
        return array

    @staticmethod
    def _gaussian_logpdf(value, covariance):
        value = np.asarray(value, dtype=float)
        sign, logdet = np.linalg.slogdet(covariance)
        if sign <= 0:
            raise ValueError("covariance must be positive definite")
        quadratic = value.T @ np.linalg.solve(covariance, value)
        dim = value.shape[0]
        return -0.5 * (dim * np.log(2.0 * np.pi) + logdet + quadratic)


def build_example_model():
    """Create a compact 2D latent / 1D observed example model."""
    transition = np.array([[0.9, 0.2], [0.0, 0.8]], dtype=float)
    observation = np.array([[1.0, 0.0]], dtype=float)
    process_cov = 0.05 * np.eye(2)
    observation_cov = np.array([[0.1]], dtype=float)
    initial_mean = np.array([0.0, 0.0], dtype=float)
    initial_cov = np.eye(2)
    return LinearStateSpaceModel(
        transition=transition,
        observation=observation,
        process_cov=process_cov,
        observation_cov=observation_cov,
        initial_mean=initial_mean,
        initial_cov=initial_cov,
    )


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    model = build_example_model()
    states, observations = model.simulate(num_steps=8, rng=rng)
    result = model.kalman_filter(observations)

    np.set_printoptions(precision=3, suppress=True)
    print("Simulated states:")
    print(states)
    print("\nObservations:")
    print(observations)
    print("\nFiltered means:")
    print(result["filtered_means"])
    print("\nLog-likelihood:", result["log_likelihood"])