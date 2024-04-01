from abc import ABC, abstractmethod

class IRestrictionsDBRepository(ABC):
    """
    Interface for the restrictions database repository.
    """
    @abstractmethod
    def add_restriction(self, restriction):
        """
        Adds a restriction to the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def remove_restriction(self, restriction):
        """
        Removes a restriction from the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_restrictions(self):
        """
        Returns a list of all restrictions in the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_restriction(self, restriction):
        """
        Returns a restriction from the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def update_restriction(self, restriction):
        """
        Updates a restriction in the database.
        """
        raise NotImplementedError