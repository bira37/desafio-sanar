# -*- coding: utf-8 -*-

"""
    mundiapi

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""


class UpdateRecipientRequest(object):

    """Implementation of the 'UpdateRecipientRequest' model.

    Request for updating a Recipient

    Attributes:
        name (string): Name
        email (string): Email
        description (string): Description
        mtype (string): Type
        status (string): Status
        metadata (dict<object, string>): Metadata

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "name":'name',
        "email":'email',
        "description":'description',
        "mtype":'type',
        "status":'status',
        "metadata":'metadata'
    }

    def __init__(self,
                 name=None,
                 email=None,
                 description=None,
                 mtype=None,
                 status=None,
                 metadata=None):
        """Constructor for the UpdateRecipientRequest class"""

        # Initialize members of the class
        self.name = name
        self.email = email
        self.description = description
        self.mtype = mtype
        self.status = status
        self.metadata = metadata


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        name = dictionary.get('name')
        email = dictionary.get('email')
        description = dictionary.get('description')
        mtype = dictionary.get('type')
        status = dictionary.get('status')
        metadata = dictionary.get('metadata')

        # Return an object of this model
        return cls(name,
                   email,
                   description,
                   mtype,
                   status,
                   metadata)


