# DSA ALGORITHM: Singly Linked List & Node Traversal
# USED FOR: Expense & Ledger Tracker history records.

class LedgerNode:
    def __init__(self, entry_id, title, amount, entry_type, date):
        self.entry_id = entry_id
        self.title = title
        self.amount = amount
        self.entry_type = entry_type  # 'income' or 'expense'
        self.date = date
        self.next = None

class LedgerLinkedList:
    def __init__(self):
        self.head = None

    def append(self, entry_id, title, amount, entry_type, date):
        """DSA: Appending to Linked List - O(N) or O(1) if tail tracked."""
        new_node = LedgerNode(entry_id, title, amount, entry_type, date)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def traverse(self):
        """DSA: Linked List Traversal - O(N)."""
        entries = []
        current = self.head
        while current:
            entries.append({
                "id": current.entry_id,
                "title": current.title,
                "amount": current.amount,
                "type": current.entry_type,
                "date": current.date
            })
            current = current.next
        return entries
