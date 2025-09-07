import sys

try:
    distance = int(sys.argv[1])
except IndexError:
    print("python ./main.py <distance>")
    exit(1)
except ValueError:
    print("provide <distance> as an integer!")
    exit(1)

# number of 16-bit symbols used to calculate mileage storage
symbols = 17

# 34 symbols, containing 488,184 Miles or "Just Broken in" from the Tundra it came from
# 00000000: 702d 702d 702d 702d 702d 702d 702d 702d  p-p-p-p-p-p-p-p-
# 00000010: 702d 702d 702d 702d 702c 702c 702c 702c  p-p-p-p-p,p,p,p,
# 00000020: 702c ffff ffff ffff ffff ffff ffff ffff  p,..............
# 00000030: ffff ffff ffff ffff ffff 0000 0000 0000  ................
# 00000040: 0000 0000                                ....
buffer = []

# distance_base = 28716
distance_base = distance // symbols

# distance_remainder = 12
distance_remainder = distance % symbols

# distance_remainder_inverse = 5
distance_remainder_inverse = symbols - distance_remainder

# 28716 = 70 2C
distance_base_hex = hex(distance_base)

# 28717 = 70 2D
distance_modulus_hex = hex(distance_base + 1)

# 28717 * 12 = 344604
buffer.extend([distance_modulus_hex] * distance_remainder)

# 28716 * 5 = 143580
buffer.extend([distance_base_hex] * distance_remainder_inverse)
# 344604 + 143580 = 488184

# mask 12 symbols containing 70 2D as 0xffff
buffer.extend([hex(65535)] * distance_remainder)

# mask 5 symbols containing 70 2C as 0x0000
buffer.extend([hex(0)] * distance_remainder_inverse)

if len(buffer) != 34:
    print(f"err: buffer should be 34 symbols, but is actually {len(buffer)}")
    print(buffer)
    exit(1)

print(f"Input Distance:      {distance}")
print(f"Base Divisor:        {distance_base_hex} ({distance_base})")
print(f"Inverse Remainder:   {distance_remainder_inverse}")
print(f"Remainder Mask:      {distance_modulus_hex} ({int(distance_modulus_hex, 16)})")
print(f"Remainder:           {distance_remainder}")
print("34 Symbol Output: \n\n#######################################")
for i in range(0, len(buffer), 8):
    row = buffer[i:i+8]
    print(" ".join(f"{int(addr, 16):04X}" for addr in row))
print("#######################################")