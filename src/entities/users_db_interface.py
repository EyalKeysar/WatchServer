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
    def get_parents(self):
        """
        Returns a list of all parents in the database.
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
    
    @abstractmethod
    def add_child(self, child, parent):
        """
        Adds a child to the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def remove_child(self, child, parent):
        """
        Removes a child from the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_children(self, parent):
        """
        Returns a list of all children in the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_child(self, child, parent):
        """
        Returns a child from the database.
        """
        raise NotImplementedError
    
    @abstractmethod
    def update_child(self, child, parent):
        """
        Updates a child in the database.
        """
        raise NotImplementedError
    
    