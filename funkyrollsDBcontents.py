import funkyrollsDBsetup

funkyrollsDBsetup.setup_database()

file = open("tags.txt", "r")
tags_list = file.readlines()

while tags_list:
    tag, subgroup, description = tags_list.pop(0).strip().split(",")
    print(tag)
    print(subgroup)
    print(description)
    funkyrollsDBsetup.add_tag(tag, subgroup, description)
file.close()
   
file = open("subgroups.txt", "r")
subgroups_list = file.readlines()

while subgroups_list:
    tag, subgroup, description = subgroups_list.pop(0).strip().split(",")
    print(tag)
    print(subgroup)
    print(description)
    funkyrollsDBsetup.add_and_connect_subgroup_tag(tag, subgroup, description)
file.close()

file = open("champions.txt", "r")
champions_list = file.readlines()

while champions_list:
    champion, release_date = champions_list.pop(0).strip().split(",")
    print(champion)
    print(release_date)
    funkyrollsDBsetup.add_champion(champion, release_date)
file.close()

