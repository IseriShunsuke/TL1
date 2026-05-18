import bpy

bl_info = {
    "name" : "レベルエディター",
    "author" : "Iseri Shunsuke",
    "version" : (1,0),
    "blender" : (3,6,1),
    "location" : "",
    "description" : "レベルエディター",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "Object",
}

def register():
    print("レベルエディター enabled")
    
def unregister():
    print("レベルエディター disabled")
    
if __name__ ==  "__main__" : 
    register()