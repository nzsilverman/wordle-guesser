def main():
    lines = []
    with open('solutions_nyt.txt', 'r') as f:
        for line in f:
            tmp =[x.strip() for x in line.split(',')]
            for word in tmp:
                lines.append(word.split('\"')[1]+"\n")

    with open('solutions_nyt_lines.txt', "w") as f:
        f.writelines(lines)

if __name__ == '__main__':
    main()
