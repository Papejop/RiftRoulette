import funkyrollsDBsetup

funkyrollsDBsetup.setup_database()

file = open("tags.txt", "r")
tags_list = file.readlines()

while tags_list:
    tag, subgroup, description = tags_list.pop(0).strip().split(",")
    funkyrollsDBsetup.add_tag(tag, subgroup, description)
file.close()
   
file = open("subgroups.txt", "r")
subgroups_list = file.readlines()

while subgroups_list:
    tag, subgroup, description = subgroups_list.pop(0).strip().split(",")
    funkyrollsDBsetup.add_and_connect_subgroup_tag(tag, subgroup, description)
file.close()

file = open("champions.txt", "r")
champions_list = file.readlines()

while champions_list:
    champion, release_date = champions_list.pop(0).strip().split(",")
    funkyrollsDBsetup.add_champion(champion, release_date)
file.close()

file = open("champion_tag_ids.txt", "r")
champion_tag_ids_list = file.readlines()

while champion_tag_ids_list:
    champion_id, tag_id, subgroup_id = champion_tag_ids_list.pop(0).strip().split(",")
    funkyrollsDBsetup.connect_champion_tag(champion_id, tag_id, subgroup_id)
file.close()



