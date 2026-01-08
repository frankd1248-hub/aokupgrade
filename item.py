from __future__ import annotations

class Item:
    
    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name
        
    def __eq__(self: Item, other: object) -> bool:
        if not isinstance(other, Item):
            return False
        if self.ID == other.ID:
            return True
        return False
    
    def __hash__(self: Item) -> int:
        return hash(self.ID)
        

def getItem(itemID: str) -> Item:
    if itemID == "dusty_bun":
        return Item(itemID, "Dusty Bun")
    else:
        return Item(itemID, f"Unknown({itemID})")
