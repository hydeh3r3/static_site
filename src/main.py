def main():
    def TextNode(text, text_type, url):
        return f"{text_type}{text}{url}"

    print(TextNode("Hello, World!", "bold", "https://boot.dev"))

if __name__ == "__main__":
    main()
