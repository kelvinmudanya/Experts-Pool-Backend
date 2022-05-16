from core.models import Country, Region

kenya = Country.objects.filter(name='Kenya').first()
rwanda = Country.objects.filter(name='Rwanda').first()
ssd = Country.objects.filter(name='South Sudan').first()
uganda = Country.objects.filter(name='Uganda').first()
tanzania = Country.objects.filter(name='Tanzania').first()
burundi = Country.objects.filter(name='Burundi').first()
congo = Country.objects.filter(name='Democratic Republic of the Congo').first()

regions = [

    Region(name='Bandundu', country=congo),
    Region(name='Équateur', country=congo),
    Region(name='Kasaï-Occidental', country=congo),
    Region(name='Kasaï-Oriental', country=congo),
    Region(name='Katanga', country=congo),
    Region(name='Orientale', country=congo),
    # burundi
    Region(name='Bubanza', country=burundi),
    Region(name='Bujumbura Mairie', country=burundi),
    Region(name='Bujumbura Rural', country=burundi),
    Region(name='Bururi', country=burundi),
    Region(name='Cankuzo', country=burundi),
    Region(name='Cibitoke', country=burundi),
    Region(name='Gitega', country=burundi),
    Region(name='Karuzi', country=burundi),
    Region(name='Kayanza', country=burundi),
    Region(name='Kirundo', country=burundi),
    Region(name='Makamba', country=burundi),
    Region(name='Muramvya', country=burundi),
    Region(name='Muyinga', country=burundi),
    Region(name='Mwaro', country=burundi),
    Region(name='Ngozi', country=burundi),
    Region(name='Rumonge', country=burundi),
    Region(name='Rutana', country=burundi),
    Region(name='Ruyigi', country=burundi),

    # tanzania
    Region(name='Arusha', country=tanzania),
    Region(name='Bagamoyo', country=tanzania),
    Region(name='Bukoba', country=tanzania),
    Region(name='Dar es Salaam', country=tanzania),
    Region(name='Dodoma', country=tanzania),
    Region(name='Iringa', country=tanzania),
    Region(name='Kilwa', country=tanzania),
    Region(name='Kondoa-Irangi', country=tanzania),
    Region(name='Lindi', country=tanzania),
    Region(name='Mahenge', country=tanzania),
    Region(name='Morogoro', country=tanzania),
    Region(name='Moshi', country=tanzania),
    Region(name='Mwanza', country=tanzania),
    Region(name='Pangani', country=tanzania),
    Region(name='Rufiji', country=tanzania),
    Region(name='Rungwe', country=tanzania),
    Region(name='Songea', country=tanzania),
    Region(name='Tabora', country=tanzania),
    Region(name='Tanga', country=tanzania),
    Region(name='Ufipa', country=tanzania),
    Region(name='Ujiji', country=tanzania),
    Region(name='Usambara', country=tanzania),

    # uganda
    Region(name='Central', country=uganda),
    Region(name='Western', country=uganda),
    Region(name='Eastern', country=uganda),
    Region(name='Nothern', country=uganda),

    # kenya
    Region(name='Central', country=kenya),
    Region(name='Coast', country=kenya),
    Region(name='Eastern', country=kenya),
    Region(name='North Eastern', country=kenya),
    Region(name='Nyanza', country=kenya),
    Region(name='Rift Valley', country=kenya),
    Region(name='Western', country=kenya),

    Region(name='Gasabo', country=rwanda),
    Region(name='Kicukiro', country=rwanda),
    Region(name='Nyarugenge', country=rwanda),
    Region(name='Bugesera', country=rwanda),
    Region(name='Gatsibo', country=rwanda),
    Region(name='Kayonza', country=rwanda),
    Region(name='Kirehe', country=rwanda),
    Region(name='Ngoma', country=rwanda),
    Region(name='Nyagatare', country=rwanda),
    Region(name='Rwamagana', country=rwanda),
    Region(name='Burera', country=rwanda),
    Region(name='Gakenke', country=rwanda),
    Region(name='Gicumbi', country=rwanda),
    Region(name='Musanze', country=rwanda),
    Region(name='Rulindo', country=rwanda),
    Region(name='Gisagara', country=rwanda),
    Region(name='Huye', country=rwanda),
    Region(name='Kamonyi', country=rwanda),
    Region(name='Muhanga', country=rwanda),
    Region(name='Nyamagabe', country=rwanda),
    Region(name='Nyanza', country=rwanda),
    Region(name='Nyaruguru', country=rwanda),
    Region(name='Ruhango', country=rwanda),
    Region(name='Karongi', country=rwanda),
    Region(name='Ngororero', country=rwanda),
    Region(name='Nyabihu', country=rwanda),
    Region(name='Nyamasheke', country=rwanda),
    Region(name='Rubavu', country=rwanda),
    Region(name='Rusizi', country=rwanda),
    Region(name='Rutsiro', country=rwanda),

    # SSD
    Region(name='Northern Bahr el Ghazal', country=ssd),
    Region(name='Western Bahr el Ghazal', country=ssd),
    Region(name='Lakes State', country=ssd),
    Region(name='Warrap', country=ssd),
    Region(name='Western Equatoria', country=ssd),
    Region(name='Central Equatoria', country=ssd),
    Region(name='Eastern Equatoria[edit]', country=ssd),
    Region(name='Jonglei', country=ssd),
    Region(name='Unity State[edit]', country=ssd),
    Region(name='Upper Nile State[edit]', country=ssd),
    Region(name='Ruweng Administrative Area', country=ssd),
    Region(name='Pibor Administrative Area', country=ssd),
    Region(name='Abyei Administrative Area', country=ssd),

]

for region in regions:
    region_obj = region.save()
