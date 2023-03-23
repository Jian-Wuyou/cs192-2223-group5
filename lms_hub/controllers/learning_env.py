from abc import abstractmethod, ABC

class LearningEnv(ABC): 
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def get_deadlines(self):
        """Returns a list of the user's requirements"""
        raise NotImplementedError

    @abstractmethod
    def get_classes(self):
        """Returns a list of the user's classes"""
        raise NotImplementedError