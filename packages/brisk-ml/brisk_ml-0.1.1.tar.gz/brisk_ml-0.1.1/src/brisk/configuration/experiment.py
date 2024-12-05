"""experiment.py

This module defines the Experiment class, which represents a single experiment 
within the Brisk framework. The Experiment dataclass store the data path, group
name and algorithms to use.
"""

import dataclasses
import hashlib
import pathlib
from typing import Dict

from brisk.utility import algorithm_wrapper

@dataclasses.dataclass
class Experiment:
    """Configuration for a single experiment run.
    
    Encapsulates all information needed for one experiment run, including 
    dataset path, model instances, and group organization. Provides validation 
    and consistent naming for experiment organization.
    
    Attributes:
        group_name: Name of the experiment group for organization
        dataset: Path to the dataset file
        algorithms: Dictionary of instantiated models with standardized keys:
                   - Single model: {"model": instance}
                   - Multiple models: {"model1": inst1, "model2": inst2, ...}
    
    Example:
        >>> from sklearn.linear_model import LinearRegression
        >>> experiment = Experiment(
        ...     group_name="baseline",
        ...     dataset=Path("data/example.csv"),
        ...     algorithms={"model": LinearRegression()}
        ... )
        >>> print(experiment.experiment_name)
        'baseline_a1b2c3d4'
    """
    group_name: str
    dataset: pathlib.Path
    algorithms: Dict[str, algorithm_wrapper.AlgorithmWrapper]

    @property
    def full_name(self) -> str:
        """Generate full descriptive name for logging and debugging.
        
        Returns:
            String combining group name and full model class names.
            Example: 'baseline_LinearRegression_RandomForestRegressor'
        """
        algo_names = "_".join(
            algo.name for algo in self.algorithms.values()
        )
        return f"{self.group_name}_{algo_names}"

    @property
    def experiment_name(self) -> str:
        """Generate a consistent, unique, and concise name for this experiment.
        
        Uses blake2b hash of full_name to create a short, unique identifier
        while maintaining consistent naming across runs.
        
        Returns:
            String in format: '{group_name}_{8_char_hash}'
            Example: 'baseline_a1b2c3d4'
        """
        hash_obj = hashlib.blake2b(self.full_name.encode(), digest_size=4)
        short_hash = hash_obj.hexdigest()
        return f"{self.group_name}_{short_hash}"

    @property
    def name(self) -> str:
        """Return a name for the experiment, prioritizing full_name if under 
        30 characters.
        
        Returns:
            String: Either full_name or experiment_name based on length.
        """
        if len(self.full_name) < 30:
            return self.full_name
        return self.experiment_name

    def __post_init__(self):
        """Validate experiment configuration after initialization.
        
        Performs the following validations:
        1. Converts dataset to Path if it's a string
        2. Validates group_name is a string
        3. Validates algorithms is a non-empty dictionary
        4. Validates model naming convention:
           - Single model must use key "model"
           - Multiple models must use keys "model1", "model2", etc.
        
        Raises:
            ValueError: If any validation fails:
                - If group_name is not a string
                - If algorithms is not a dictionary
                - If algorithms is empty
                - If model keys don't follow naming convention
        """
        if not isinstance(self.dataset, pathlib.Path):
            self.dataset = pathlib.Path(self.dataset)

        if not isinstance(self.group_name, str):
            raise ValueError("Group name must be a string")

        if not isinstance(self.algorithms, dict):
            raise ValueError("Algorithms must be a dictionary")

        if not self.algorithms:
            raise ValueError("At least one algorithm must be provided")

        # Validate model naming convention
        if len(self.algorithms) == 1:
            if list(self.algorithms.keys()) != ["model"]:
                raise ValueError('Single model must use key "model"')
        else:
            expected_keys = [
                "model" if i == 0 else f"model{i+1}" 
                for i in range(len(self.algorithms))
            ]
            if list(self.algorithms.keys()) != expected_keys:
                raise ValueError(
                    f"Multiple models must use keys {expected_keys}"
                )

    def get_model_kwargs(self) -> Dict[str, algorithm_wrapper.AlgorithmWrapper]:
        """Get models in the format expected by workflow.
        
        Returns:
            Dictionary of model instances with standardized keys.
            For single model: {"model": instance}
            For multiple models: {"model": inst1, "model2": inst2, ...}
        """
        return self.algorithms
