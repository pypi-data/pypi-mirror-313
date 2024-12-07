x = [4, 3, 36, 11, 4, 3, 36, 10, 4, 3, 36, 9, 4, 3, 36, 8, 5, 1, 2, 3, 4]\

frame_length = len(x)

# get first byte which is the report length
while frame_length:
    report_length = x[0]
    frame_length = frame_length - report_length

    # slide off first byte
    x = x[0::]
    for z in range(report_length ):
        print(x[z])
    x = x[report_length::]
    print(x)

print('done')

