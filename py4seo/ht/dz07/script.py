import web_classes

main_info_section_title = web_classes.Title("Main info")
extra_info_section_title = web_classes.Title("Extra info").with_level(2)

name = web_classes.Text("name - Vasiliy")
nick = web_classes.Text("nick - vvscode")

avatar_image = web_classes.Image("https://purr.objects-us-east-1.dream.io/i/Q8WvU.jpg")
linked_image = web_classes.Link(
    web_classes.Image("https://purr.objects-us-east-1.dream.io/i/WzNoP.jpg")
).with_anchor("https://random.cat/view/124")

main_page = web_classes.Page(main_info_section_title, name, nick, avatar_image)

sub_page = web_classes.Page(extra_info_section_title, linked_image)
sub_page.add_to_header(web_classes.Description("Awesome sub page"))

website = web_classes.Website()
website.add_page("/", main_page)
website.add_page("/img", sub_page)
website.set_not_found(web_classes.Page(web_classes.Text("Nothing here")))

book = web_classes.Book(main_page, sub_page)

print("Start")

print("HTML versions for pages")
print("Website navigate to /:", website.navigate("/").html)
print("Website navigate to /img:", website.navigate("/img").html)
print(
    "Website navigate to /some_ukknownpage:", website.navigate("/some_ukknownpage").html
)

print("Text versions for pages:")
print("Website navigate to /:", website.navigate("/").text)
print("Website navigate to /img:", website.navigate("/img").text)
print(
    "Website navigate to /some_ukknownpage:", website.navigate("/some_ukknownpage").text
)

print("Book:")
print(book)
