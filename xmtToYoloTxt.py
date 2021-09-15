# -*- coding: utf-8 -*-
from xml.dom import minidom
import os
import glob

cls_label = {}
cls_label['with_mask'] = 0 # <name>with_mask</name>
cls_label['without_mask'] = 1 # <name>without_mask</name>
cls_label['mask_weared_incorrect'] = 2 # <name>mask_weared_incorrect</name>


#ToDo: 
#One Row Per object
#Each Row is class x_center y_center width height format (normalized)
# Normalized Range: from 0 - 1

# size ~ dimension of the image; size[0] – width size[1] – height
# box ~ xml bounding box coordinates box ~ [xmin, ymin, xmax, and ymax]
def normalize_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x_ctr =  (box[0]+box[2])/2.0  #(xmin+xmax)/2.0
    y_ctr =  (box[1]+box[3])/2.0  #(ymin+ymax)/2.0
    bbox_w = box[2] - box[0]   # xmax - xmin
    bbox_h = box[3] - box[1]  # ymax - ymin
    norm_x_ctr = x_ctr*dw  #normalized x_center point
    norm_y_ctr = y_ctr*dh #normalized y_center_point
    norm_bbox_w = bbox_w*dw # normalized bbox_width
    norm_bbox_h = bbox_h*dh #normalized bbox_height
    return norm_x_ctr, norm_y_ctr, norm_bbox_w, norm_bbox_h

 #ToDo:
 # traverse every single xml file and convert all to *.txt
 # cls_label: {'class 1': 0, 'class 2': 1, 'class 3': 2, ..., 'class n': n-1 }
def xml_to_txt_converter( cls_label ):
    save_path = os.getcwd()+'/labels'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        print('New directory created: {}'.format(save_path))


    for file_name in glob.glob('*.xml'):
        xmldoc = minidom.parse(file_name)
        file_name_out =(file_name[:-4]+ '.txt')
        file_name_out = os.path.join(save_path, file_name_out)
        
        with open(file_name_out, 'w') as f:

            image_size_items = xmldoc.getElementsByTagName('size')[0]
            object_items = xmldoc.getElementsByTagName('object')

            print('debug: printing object <name> in this xml file :')
            for obj_item in object_items:
                print(obj_item.getElementsByTagName('name')[0].firstChild.data)
            image_width = int(image_size_items.getElementsByTagName('width')[0].firstChild.data)
            image_height = int(image_size_items.getElementsByTagName('height')[0].firstChild.data)
            
            print('debug: printing image_size_items in this xml file:')
            print('Image Width: {},  Image Height: {}'.format(image_width, image_height))
            for object_item in object_items:
                cls_id = (object_item.getElementsByTagName('name')[0].firstChild.data)
                if cls_id in cls_label:
                    label_string = str(cls_label[cls_id])
                    print('Label_string: {}'.format(label_string))
                else:
                    label_string ="-1"
                    print("No Such a Label!")
                x_min = (object_item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0].firstChild.data  
                y_min = (object_item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0].firstChild.data  
                x_max = (object_item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0].firstChild.data  
                y_max = (object_item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0].firstChild.data  
                bbox = (float(x_min), float(y_min), float(x_max), float(y_max))
                normalization = normalize_coordinates((image_width, image_height), bbox)
                print('Normalized Annotation: {}'.format(normalization))
                print(label_string + " " + " ".join([("%.6f" % a) for a in normalization]) + '\n')
                f.write(label_string + " " + " ".join([("%.6f" % a) for a in normalization]) + '\n')

            
           
"""
 Getting bounding box information: object_item[] ['name', ...,'bndbox']           
            x_min = object_item.getElementsByTagName('bndbox')[0].getElementsByTagName('xmin')[0].firstChild.data
            y_min = object_item.getElementsByTagName('bndbox')[0].getElementsByTagName('ymin')[0].firstChild.data
            x_max = object_item.getElementsByTagName('bndbox')[0].getElementsByTagName('xmax')[0].firstChild.data
            y_max = object_item.getElementsByTagName('bndbox')[0].getElementsByTagName('ymax')[0].firstChild.data

            bbox = (float(x_min),float(y_min),float(x_max),float(y_max))
            normalization = normalize_coordinates((image_width, image_height), bbox)
            print('Normalized annotation: {}'.format(normalization))
            print('Yolo *.txt format:   ')
            print(label_string + " " + " ".join([("%.6f" % a) for a in normalization]) + '\n')

            f.write(label_string + " " + " ".join([("%.6f" % a) for a in normalization]) + '\n')
            print('Conversion done!  %s' % file_name_out)
 """             
#
        
         



def main():
    #size = [1280,1280]
    #box =[567, 365, 865, 455]
    #print(normalize_coordinates(size, box))
    print('--------------------------------testing on xml2txt--------------------------------')
    #print(cls_label)
    xml_to_txt_converter( cls_label )

if __name__ == "__main__":
    main()




 
 