from cltl.dialogue_evaluation import logger


class BasicEvaluator(object):

    def __init__(self):
        # type: () -> None
        """
        Generate evaluation

        Parameters
        ----------
        """

        self._log = logger.getChild(self.__class__.__name__)
        self._log.info("Booted")

    def evaluate_conversation(self, scenario_folder, rdf_folder):
        raise NotImplementedError()


class BasicPlotter(object):

    def __init__(self):
        # type: () -> None
        """
        Visually compare dialogue evaluations

        Parameters
        ----------
        """

        self._log = logger.getChild(self.__class__.__name__)
        self._log.info("Booted")

    def plot_conversations(self, scenarios_paths, metrics):
        raise NotImplementedError()


class BasicCorrelator(object):

    def __init__(self):
        # type: () -> None
        """
        Compute correlations between different dialogue evaluations

        Parameters
        ----------
        """

        self._log = logger.getChild(self.__class__.__name__)
        self._log.info("Booted")

    def correlate_metrics(self, scenarios_paths, metrics):
        raise NotImplementedError()

