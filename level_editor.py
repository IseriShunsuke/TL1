import bpy
import math
import bpy_extras

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

class MYADDON_OT_add_file_name(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName 追加"
    bl_description = "[Filename]カスタムプロパティを追加します"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context): 
        context.object["file_name"] = ""

        return {'FINISHED'}

class OBJECT_PT_file_name(bpy.types.Panel):
    """オブジェクトのファイルネームパネル"""
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self,context):
        if "file_name" in context.object:
            self.layout.prop(context.object,'["file_name"]', text=self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_file_name.bl_idname)
    

class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    filename_ext = ".scene"

    def parse_scene_recursive(self, file, object, level):
        """シーン回帰関数"""

        indent = ''
        for i in range(level):
            indent += "\t"

       
        self.write_and_print(file, indent +  object.type)
        trans, rot, scale = object.matrix_local.decompose()

        rot = rot.to_euler()

        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        self.write_and_print(file, indent + "T %f %f %f)" % (trans.x,trans.y,trans.z))
        self.write_and_print(file, indent + "R %f %f %f)" % (rot.x,rot.y,rot.z))
        self.write_and_print(file, indent + "S %f %f %f)" % (scale.x,scale.y,scale.z))
        self.write_and_print(file,'')

        if "file_name" in object:
            self.write_and_print(file, indent + "N %s" % object["file_name"])
        self.write_and_print(file, indent + "END")
        self.write_and_print(file, '')

        for child in object.children:
            self.parse_scene_recursive(file,child,level + 1)

    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')

    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始…%r" % self.filepath)

        with open(self.filepath, "wt") as file:
            file.write("SCENE\n")

            for object in bpy.context.scene.objects:
                if object.parent:
                    continue
                
                self.parse_scene_recursive(file, object, 0)

            

    def execute(self,context):
         
         print("シーン情報をExportします")

         self.export()

         print("シーン情報をExportしました")
         self.report({'INFO'},"シーン情報をExportしました")

         return {'FINISHED'}





class MYADDON_OT_strech_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_strech_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context): 
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")

        return {'FINISHED'}

class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context): 
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")

        return {'FINISHED'}


class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    
    bl_label = "MyMenu"
    
    bl_description = "拡張メニュー by" + bl_info["author"]
    
    def draw(self, context):
        self.layout.operator("wm.url_open_preset", 
            text="Manual", icon="HELP")
        self.layout.operator(MYADDON_OT_strech_vertex.bl_idname, 
            text=MYADDON_OT_strech_vertex.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, 
            text=MYADDON_OT_export_scene.bl_label)


    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

classes = (
    MYADDON_OT_export_scene,
    MYADDON_OT_strech_vertex,
    MYADDON_OT_create_ico_sphere,
    TOPBAR_MT_my_menu,
    OBJECT_PT_file_name,
    MYADDON_OT_add_file_name
)
        

def draw_menu_manual(self,context): 
    self.layout.operator("wm.url_open_preset", text="Manual", icon="HELP")
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディターが有効化されました")
    
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディターが無効化されました")
    
if __name__ ==  "__main__" : 
    register()
    
