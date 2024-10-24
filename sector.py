class Sector:
    """
    Class to represent a sector of interest for monitoring social media content.
    
    Attributes:
    - name: str, the name of the sector.
    - departments: array, departments responsible for addressing concerns related to the sector.
    """
    def __init__(self, sector, departments):
        self.sector = sector
        self.departments = departments

