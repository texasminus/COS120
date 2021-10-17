import urllib.request		#pip install concat("urllib", number of current version)

my_request = urllib.request.urlopen("https://www.google.com/search?q=touring+bicycles&rlz=1C1GCEB_enUS969US969&sxsrf=AOaemvI3VRkrob24x_vkywg6wtxjvgz20A%3A1634501465418&ei=WYNsYfvkGJusqtsP59WpmAU&oq=touring+bicycles&gs_lcp=Cgdnd3Mtd2l6EAMYAzIECCMQJzIECCMQJzIECCMQJzIFCAAQkQIyBQgAEJECMgUIABCRAjIFCAAQkQIyCAgAEIAEEMkDMgUIABCABDIFCAAQgAQ6CAgAEIAEELEDOgQIABBDSgQIQRgAULECWLgFYPAPaABwAngAgAGrAYgB4wOSAQMzLjKYAQCgAQHAAQE&sclient=gws-wiz")

my_HTML = my_request.read().decode("utf-8")

print(my_HTML)