# Assignment 03 — CHANGES

**Name:** Thet Htoo Naing  **Student ID:** 6705140009

## 1 · What I changed

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Products, order records, and items were tuples. | Added `Product`, `OrderItem`, `Customer`, and `Order` objects. | Classes and composition | Ran `python Assignment_03.py`; self-test printed PASS. |
| 2 | Discount and points used tier condition chains. | Added `NoneCustomer`, `SilverCustomer`, `GoldCustomer`, and `PlatinumCustomer` subclasses. | Inheritance and polymorphism | Compared the refactored output with the locked legacy output; PASS. |
| 3 | State was not validated when records were created. | Constructors validate names, prices, quantities, products, customers, and orders. | Encapsulation | Checked invalid values raise `ValueError`; normal data still printed PASS. |
| 4 | Calculation and receipt printing were mixed together. | `subtotal`, `discount`, `tax`, `total`, and `points` return values; `receipt` formats the output. | Pure methods and interface separation | Captured both outputs and compared them line by line; PASS. |
| 5 | Tax logic and numeric literals were repeated or unnamed. | Products provide their tax rate, and shared values are named constants. | Encapsulation and clean implementation | Ran the complete self-test and inspected every receipt line; PASS. |

## 2 · Short reflection

The biggest improvement was replacing the tier condition chains with customer subclasses. Each tier now owns its discount rates and points multiplier, so the order only asks the customer for the result. Composition also makes the relationships clear because an order has a customer and order items, while each item has a product. Keeping the behaviour identical required preserving the original receipt wording, line order, rounding, and blank lines. I verified this by capturing the legacy and refactored output and requiring an exact string match.

## 3 · Prompt log (Level 2)

| # | My prompt to the AI | What it suggested (summary) | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | Refactor the supplied store program into classes without changing its output. | Suggested domain classes for products, items, customers, and orders. | Edited | Read the class relationships and ran the self-test. |
| 2 | Replace the tier discount and points chains with polymorphism. | Suggested a customer base class with one subclass per tier. | Edited | Checked every tier's rates and multipliers against the assignment rules. |
| 3 | Separate pure calculations from receipt formatting and preserve exact output. | Suggested return-valued calculation methods and a receipt builder. | Accepted with edits | Compared captured output with the legacy golden output; PASS. |
| 4 | Complete the change table and reflection based on the implemented refactor. | Suggested concise explanations of the OOP changes and verification. | Edited | Confirmed each row matches code that is actually present. |

**Ownership statement.** By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.

## 4 · Before-you-submit checklist

- [x] `python Assignment_03.py` prints **PASS**.
- [x] No tuples / parallel lists are used for products, orders, and items in the refactored design.
- [x] Tier behaviour is implemented by a class family.
- [x] Calculation methods return values and receipt formatting is separate.
- [x] Constructors validate state and named constants replace shared magic numbers.
- [x] The change table and reflection are filled in.
- [x] The prompt log is complete and the ownership statement is included.
