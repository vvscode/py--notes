def chees_and_crackers(cheese_count, boxes_of_crackers):
  print(f"You have {cheese_count} cheeses!")
  print(f"You have {boxes_of_crackers} boxes of crackers!")
  print(f"Man that's enough for a party!")
  print()

print(f"We can just give the function numbers directly:")
chees_and_crackers(20, 30)

print(f"Or, we can use variables from script")
x = 10
y = 50
chees_and_crackers(x, y)

print(f"Or, use expressions or mix")
chees_and_crackers(x + 10, 44)

print(f"Or use list, for example")
chees_and_crackers(*[1, 2])