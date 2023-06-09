import csv

from core.models import Competence, Specialization

# exec(open('core/insert_regions.py').read())


# kenya = Country.objects.filter(name='Kenya').first()
# rwanda = Country.objects.filter(name='Rwanda').first()
# ssd = Country.objects.filter(name='South Sudan').first()
# uganda = Country.objects.filter(name='Uganda').first()
# tanzania = Country.objects.filter(name='Tanzania').first()
# burundi = Country.objects.filter(name='Burundi').first()
# congo = Country.objects.filter(name='Democratic Republic of the Congo').first()
#
# regions = [
#
#     Region(name='Bandundu', country=congo),
#     Region(name='Équateur', country=congo),
#     Region(name='Kasaï-Occidental', country=congo),
#     Region(name='Kasaï-Oriental', country=congo),
#     Region(name='Katanga', country=congo),
#     Region(name='Orientale', country=congo),
#     # burundi
#     Region(name='Bubanza', country=burundi),
#     Region(name='Bujumbura Mairie', country=burundi),
#     Region(name='Bujumbura Rural', country=burundi),
#     Region(name='Bururi', country=burundi),
#     Region(name='Cankuzo', country=burundi),
#     Region(name='Cibitoke', country=burundi),
#     Region(name='Gitega', country=burundi),
#     Region(name='Karuzi', country=burundi),
#     Region(name='Kayanza', country=burundi),
#     Region(name='Kirundo', country=burundi),
#     Region(name='Makamba', country=burundi),
#     Region(name='Muramvya', country=burundi),
#     Region(name='Muyinga', country=burundi),
#     Region(name='Mwaro', country=burundi),
#     Region(name='Ngozi', country=burundi),
#     Region(name='Rumonge', country=burundi),
#     Region(name='Rutana', country=burundi),
#     Region(name='Ruyigi', country=burundi),
#
#     # tanzania
#     Region(name='Arusha', country=tanzania),
#     Region(name='Bagamoyo', country=tanzania),
#     Region(name='Bukoba', country=tanzania),
#     Region(name='Dar es Salaam', country=tanzania),
#     Region(name='Dodoma', country=tanzania),
#     Region(name='Iringa', country=tanzania),
#     Region(name='Kilwa', country=tanzania),
#     Region(name='Kondoa-Irangi', country=tanzania),
#     Region(name='Lindi', country=tanzania),
#     Region(name='Mahenge', country=tanzania),
#     Region(name='Morogoro', country=tanzania),
#     Region(name='Moshi', country=tanzania),
#     Region(name='Mwanza', country=tanzania),
#     Region(name='Pangani', country=tanzania),
#     Region(name='Rufiji', country=tanzania),
#     Region(name='Rungwe', country=tanzania),
#     Region(name='Songea', country=tanzania),
#     Region(name='Tabora', country=tanzania),
#     Region(name='Tanga', country=tanzania),
#     Region(name='Ufipa', country=tanzania),
#     Region(name='Ujiji', country=tanzania),
#     Region(name='Usambara', country=tanzania),
#
#     # uganda
#     Region(name='Central', country=uganda),
#     Region(name='Western', country=uganda),
#     Region(name='Eastern', country=uganda),
#     Region(name='Nothern', country=uganda),
#
#     # kenya
#     Region(name='Central', country=kenya),
#     Region(name='Coast', country=kenya),
#     Region(name='Eastern', country=kenya),
#     Region(name='North Eastern', country=kenya),
#     Region(name='Nyanza', country=kenya),
#     Region(name='Rift Valley', country=kenya),
#     Region(name='Western', country=kenya),
#
#     Region(name='Gasabo', country=rwanda),
#     Region(name='Kicukiro', country=rwanda),
#     Region(name='Nyarugenge', country=rwanda),
#     Region(name='Bugesera', country=rwanda),
#     Region(name='Gatsibo', country=rwanda),
#     Region(name='Kayonza', country=rwanda),
#     Region(name='Kirehe', country=rwanda),
#     Region(name='Ngoma', country=rwanda),
#     Region(name='Nyagatare', country=rwanda),
#     Region(name='Rwamagana', country=rwanda),
#     Region(name='Burera', country=rwanda),
#     Region(name='Gakenke', country=rwanda),
#     Region(name='Gicumbi', country=rwanda),
#     Region(name='Musanze', country=rwanda),
#     Region(name='Rulindo', country=rwanda),
#     Region(name='Gisagara', country=rwanda),
#     Region(name='Huye', country=rwanda),
#     Region(name='Kamonyi', country=rwanda),
#     Region(name='Muhanga', country=rwanda),
#     Region(name='Nyamagabe', country=rwanda),
#     Region(name='Nyanza', country=rwanda),
#     Region(name='Nyaruguru', country=rwanda),
#     Region(name='Ruhango', country=rwanda),
#     Region(name='Karongi', country=rwanda),
#     Region(name='Ngororero', country=rwanda),
#     Region(name='Nyabihu', country=rwanda),
#     Region(name='Nyamasheke', country=rwanda),
#     Region(name='Rubavu', country=rwanda),
#     Region(name='Rusizi', country=rwanda),
#     Region(name='Rutsiro', country=rwanda),
#
#     # SSD
#     Region(name='Northern Bahr el Ghazal', country=ssd),
#     Region(name='Western Bahr el Ghazal', country=ssd),
#     Region(name='Lakes State', country=ssd),
#     Region(name='Warrap', country=ssd),
#     Region(name='Western Equatoria', country=ssd),
#     Region(name='Central Equatoria', country=ssd),
#     Region(name='Eastern Equatoria[edit]', country=ssd),
#     Region(name='Jonglei', country=ssd),
#     Region(name='Unity State[edit]', country=ssd),
#     Region(name='Upper Nile State[edit]', country=ssd),
#     Region(name='Ruweng Administrative Area', country=ssd),
#     Region(name='Pibor Administrative Area', country=ssd),
#     Region(name='Abyei Administrative Area', country=ssd),
#
# ]
#
# for region in regions:
#     region_obj = region.save()
# occupations = [
# Occupation(name='Computer Scientist', occupation_category_id=10),
# Occupation(name='Anthropology', occupation_category_id=OccupationCategory.objects.filter(name='Anthropology').first().id),
# Occupation(name='Environmental expert ',
#            occupation_category_id=OccupationCategory.objects.filter(name='Environment').first().id),
# Occupation(name='Veterinarian',
#            occupation_category_id=OccupationCategory.objects.filter(name='Animal Health Sector').first().id),
# Occupation(name='Animal scientist',
#            occupation_category=OccupationCategory.objects.filter(name='Animal Health Sector').first().id),
# Occupation(name='Wildlife Science', occupation_category_id=OccupationCategory.objects.filter(name='Wildlife').first().id)
#
# ]
#
# for occupation in occupations:
#     occupation.save()
#
#
# Specialization.objects.bulk_create([
# Specialization.objects.create(name="Computer Service and Operation", occupation_id=10),
# Specialization.objects.create(name="GIS", occupation_id=10),
# Specialization.objects.create(name="Software Engineering", occupation_id=10),
# Specialization.objects.create(name="Computer Applications", occupation_id=10),
# Specialization.objects.create(name="International Trade & Business", occupation_id=11),
# Specialization.objects.create(name="Trade value chains Safe trade Food Standards", occupation_id=11),
# Specialization.objects.create(name="International Relations", occupation_id=11),
# Specialization.objects.create(name="Health issues", occupation_id=12),
#
# Specialization.objects.create("Environmental studies", occupation_id=3),
# Specialization.objects.create("Environmental & Biological conservation", occupation_id=3),
# Specialization.objects.create("Pollution Prevention and Restoration.", occupation_id=3),
# Specialization.objects.create("Ecology", occupation_id=3),
# Specialization.objects.create("Environment Health", occupation_id=3),
# Specialization.objects.create("Environment and Natural Resources", occupation_id=3),
#
#
#
#
#
# ])
#
# occupation = Occupation.objects.filter(name="Veterinarian").first()
#
#
# sp =["Epidemiology",
# "Field Veterinarian",
# "Pathologisty",
# "Entomology",
# "Parasitology",
# "Veterinary laboratory expert",
# "Animal Health information management expert",
# "Wildlife Health",
# "Veterinary Public Health",
# "Livestock identification and traceability expert",
# "Veterinary immunology",
# "Veterinary pharmacology",
# "Veterinary toxicology",
# "Aquatic Health Specialist",
# "Animal Health communication expert",]
#
# for s in sp:
#     Specialization.objects.create(name=s, occupation_id=occupation.id)
#
#
# occupation2 = Occupation.objects.filter(name="Animal scientist").first()
#
# sp2=[
# "Animal Science/ Production",
# "Animal Nutrition",
# "Livestock production systems",
# ]
#
#
# occupation3 = Occupation.objects.filter(name="Animal scientist").first()
#
#
# sp3=["Ecology",
# "Wildlife Management",
# "Range Management",]
#
# for s in sp2:
#     Specialization.objects.create(name=s, occupation_id=occupation3.id)
#

with open('matrix1.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        try:
            specialization_id = Specialization.objects.get(name=row["specialization"].strip()).id
        except:
            print("failed for specialization", row["specialization"])
            continue

        if row["competencies"] != "":
            Competence.objects.create(name=row["competencies"].strip(), specialization_id=specialization_id)

        line_count += 1
        
    print(f'Processed {line_count} lines.')
