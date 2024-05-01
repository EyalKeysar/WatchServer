from abc import ABC, abstractmethod

class IUsersDBRepository(ABC):
    """
    Interface for users database repository.
    """
    @abstractmethod
    def add_parent(self, parent):
        """
        Adds a parent to the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def remove_parent(self, parent):
        """
        Removes a parent from the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_parent(self, parent):
        """
        Returns a parent from the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def update_parent(self, parent):
        """
        Updates a parent in the database.
        """
        raise NotImplementedError