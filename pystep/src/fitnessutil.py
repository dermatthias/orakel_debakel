"""
fitnessutil
===========
Contains different methods used for problem specific fitness functions.
These are domain dependent utilities that are used for computing the fitness 
function. e.g. the problem is about reading a list of motion capture frames and
we need a function that gives indexes of different groups of frames.   

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@author: by Mehdi Khoury
@version: 1.00
@copyright: (c) 2009 Mehdi Khoury under the mit license
http://www.opensource.org/licenses/mit-license.html
@contact: mehdi.khoury at gmail.com
"""

import timeit
import psyco
import random
import copy
#import settings
#import tutorial8
import csv

psyco.profile()

def GetIndexesOfGroupsInList(ml):
    """
    Function:  GetIndexesOfGroupsInList
    ===================================
    finds groups of identical elements in a list and gives their starting and last indexes. 
    
 
    @param ml: a list of elements. e.g. ml=[1,1,1,1,1,2,2,3,4,5,5,5,6]
    
    returns: A list of tuples, where each tuple is of the form 
    (group_discrete_val,group_first_ind,group_last_ind). 
    e.g.  [(1, 0, 4), (2, 5, 6), (3, 7, 7), (4, 8, 8), (5, 9, 11), (6, 12, 12)]
 
    """ 
    temp=ml[0]
    output=[]
    group_discrete_val=temp
    group_first_ind=0
    group_last_ind=0
    for i in xrange(1,len(ml)):
        if ml[i]==temp:
            group_last_ind=group_last_ind+1
        if ml[i]!=temp:
            output.append((group_discrete_val,group_first_ind,group_last_ind))
            temp=ml[i]
            group_discrete_val=temp
            group_first_ind=i
            group_last_ind=i
        if i==len(ml)-1:
            output.append((group_discrete_val,group_first_ind,group_last_ind))
    return output

def GetInputDataFromFile(myfile):
    ifile  = open(myfile, "rb")
    reader = csv.reader(ifile, delimiter="\t")
    data=[]
    rownum = 0
    for row in reader:
        mystrline= row[0]
        y = eval(mystrline.strip()) 
        data.append(GetIndexesOfGroupsInList(list(y)))
    ifile.close()
    return data

def ReplaceUsingBinaryMask(listElem,binarymask,initial,replacement ):
    try:
        
        result=copy.deepcopy(listElem)
        for i in xrange(len(listElem)):
            for j in xrange(len(listElem[i][0])):
                #print listElem[i][0][j][0]
                if listElem[i][0][j][0]==initial and binarymask[i][j]:
                    result[i][0][j]=(replacement,listElem[i][0][j][1],listElem[i][0][j][2])
                
        return result    
    except:
        raise WrongValues, "Wrong values sent to function node.\nCan't get result"
        exit

def UncompressList(listTuples):
    result=[]
    for elem in listTuples:
        #temp=[]
        for i in xrange(elem[1],elem[2]+1):
            result.append(elem[0])
    return result

if __name__ == '__main__':
    #ifile  = open('python_testdata/Boxer3_11_2TestData.csv', "rb")
    #reader = csv.reader(ifile, delimiter="\t")
    
    #rownum = 0
    #for row in reader:
    #    mystrline= row[0]
    #    y = eval(mystrline.strip()) 
    #    print GetIndexesOfGroupsInList(list(y))
    
    #ifile.close()
    print 'ok'
    Boxer1_1_1TestData=GetInputDataFromFile('python_testdata/Boxer1_1_1TestData.csv')
    #print ReplaceWithBinaryMask(settings.inputdata,tutorial8.IsLong(settings.inputdata),7,1)
    
#    Boxer1_1_1IdealData=[(7, 0, 26), (1, 27, 57), (7, 58, 155), (1, 156, 192), (7, 193, 287), (1, 288, 327), (7, 328, 414), (1, 415, 452), (7, 453, 665)]   
#    Boxer1_1_2IdealData=[(7, 0, 16), (1, 17, 70), (7, 71, 155), (1, 156, 211), (7, 212, 294), (1, 295, 349), (7, 350, 426), (1, 427, 487), (7, 488, 960)]
#
#    Boxer1_3_1IdealData=[(7, 0, 37), (6, 38, 80), (7, 81, 169), (6, 170, 214), (7, 215, 316), (6, 317, 364), (7, 365, 453), (6, 454, 500), (7, 501, 637)]
#    Boxer1_3_2IdealData=[(7, 0, 50), (6, 51, 101), (7, 102, 208), (6, 209, 264), (7, 265, 371), (6, 372, 430), (7, 431, 536), (6, 537, 591), (7, 592, 770)]
#    
#    Boxer1_5_1IdealData=[(7, 0, 65), (3, 66, 122), (7, 123, 233), (3, 234, 284), (7, 285, 399), (3, 400, 453), (7, 454, 571), (3, 572, 624), (7, 625, 751)]
#    Boxer1_5_2IdealData=[(7, 0, 52), (3, 53, 120), (7, 121, 222), (3, 223, 291), (7, 292, 403), (3, 404, 473), (7, 474, 579), (3, 580, 643), (7, 644, 769)]
#
#    Boxer1_7_1IdealData=[(7, 0, 2), (2, 3, 67), (7, 68, 185), (2, 186, 254), (7, 255, 375), (2, 376, 447), (7, 448, 561), (2, 562, 631), (7, 632, 796)]
#    Boxer1_7_2IdealData=[(7, 0, 61), (2, 62, 129), (7, 130, 238), (2, 239, 304), (7, 305, 419), (2, 420, 488), (7, 489, 616), (2, 617, 680), (7, 681, 801)]
#
#    Boxer1_8_1IdealData=[(7, 0, 34), (5, 35, 142), (7, 143, 214), (5, 215, 327), (7, 328, 407), (5, 408, 517), (7, 518, 604), (5, 605, 705), (7, 706, 801)]
#    Boxer1_8_2IdealData=[(7, 0, 76), (5, 77, 171), (7, 172, 270), (5, 271, 354), (7, 355, 454), (5, 455, 550), (7, 551, 644), (5, 645, 747), (7, 748, 876)]
#    
#    Boxer1_11_1IdealData=[(7, 0, 65), (1, 66, 83), (7, 84, 86), (6, 87, 123), (7, 124, 263), (1, 264, 282), (7, 283, 285), (6, 286, 322), (7, 323, 467), (1, 468, 486), (7, 487, 490), (6, 491, 529), (7, 530, 677), (1, 678, 699), (6, 700, 738), (7, 739, 861)]
#    Boxer1_11_2IdealData=[(7, 0, 87), (1, 88, 110), (7, 111, 116), (6, 117, 167), (7, 168, 336), (1, 337, 356), (7, 357, 364), (6, 365, 416), (7, 417, 568), (1, 569, 589), (7, 590, 597), (6, 598, 650), (7, 651, 809), (1, 810, 832), (7, 833, 837), (6, 838, 888), (7, 889, 1015)]
#    
#    Boxer1_14_1IdealData=[(7, 0, 84), (1, 85, 100), (3, 101, 159), (7, 160, 358), (1, 359, 380), (3, 381, 442), (7, 443, 623), (1, 624, 642), (3, 643, 702), (7, 703, 864), (1, 865, 882), (3, 883, 940), (7, 941, 1068)]
#    Boxer1_14_2IdealData=[(7, 0, 73), (1, 74, 88), (7, 89, 94), (3, 95, 165), (7, 166, 311), (1, 312, 326), (7, 327, 333), (3, 334, 401), (7, 402, 546), (1, 547, 569), (7, 570, 572), (3, 573, 642), (7, 643, 793), (1, 794, 811), (7, 812, 818), (3, 819, 887), (7, 888, 1015)]
#
#    Boxer1_15_1IdealData=[(7, 0, 62), (1, 63, 73), (7, 74, 83), (6, 84, 104), (7, 105, 109), (2, 110, 153), (7, 154, 338), (1, 339, 355), (6, 356, 381), (7, 382, 383), (2, 384, 435), (7, 436, 603), (1, 604, 620), (7, 621, 623), (6, 624, 646), (2, 647, 707), (7, 708, 907), (1, 908, 924), (7, 925, 928), (6, 929, 950), (7, 951, 956), (2, 957, 1007), (7, 1008, 1184)]
#    Boxer1_15_2IdealData=[(7, 0, 99), (1, 100, 117), (7, 118, 130), (6, 131, 158), (7, 159, 163), (2, 164, 218), (7, 219, 412), (1, 413, 430), (7, 431, 439), (6, 440, 476), (7, 477, 482), (2, 483, 538), (7, 539, 751), (1, 752, 771), (7, 772, 782), (6, 783, 821), (7, 822, 826), (2, 827, 886), (7, 887, 1092), (1, 1093, 1110), (7, 1111, 1122), (6, 1123, 1151), (7, 1152, 1157), (2, 1158, 1214), (7, 1215, 1451)]
#
#    Boxer2_1_1IdealData=[(7, 0, 170), (1, 171, 189), (7, 190, 312), (1, 313, 329), (7, 330, 451), (1, 452, 472), (7, 473, 585), (1, 586, 612), (7, 613, 763)]
#    Boxer2_1_2IdealData=[(7, 0, 244), (1, 245, 279), (7, 280, 404), (1, 405, 445), (7, 446, 561), (1, 562, 613), (7, 614, 724), (1, 725, 772), (7, 773, 940)]
#    
#    Boxer2_3_1IdealData=[(7, 0, 135), (6, 136, 185), (7, 186, 316), (6, 317, 374), (7, 375, 492), (6, 493, 549), (7, 550, 656), (6, 657, 713), (7, 714, 876)]
#    Boxer2_3_2IdealData=[(7, 0, 148), (6, 149, 218), (7, 219, 339), (6, 340, 408), (7, 409, 530), (6, 531, 600), (7, 601, 715), (6, 716, 783), (7, 784, 918)]
#
#    Boxer2_5_1IdealData=[(7, 0, 153), (3, 154, 203), (7, 204, 326), (3, 327, 377), (7, 378, 496), (3, 497, 545), (7, 546, 665), (3, 666, 724), (7, 725, 851)]
#    Boxer2_5_2IdealData=[(7, 0, 145), (3, 146, 199), (7, 200, 339), (3, 340, 392), (7, 393, 517), (3, 518, 573), (7, 574, 692), (3, 693, 753), (7, 754, 885)]
#
#    Boxer2_7_1IdealData=[(7, 0, 133), (2, 134, 169), (7, 170, 333), (2, 334, 386), (7, 387, 531), (2, 532, 589), (7, 590, 730), (2, 731, 791), (7, 792, 908)]
#    Boxer2_7_2IdealData=[(7, 0, 139), (2, 140, 178), (7, 179, 346), (2, 347, 389), (7, 390, 544), (2, 545, 581), (7, 582, 737), (2, 738, 788), (7, 789, 907)]
#
#    Boxer2_8_1IdealData=[(7, 0, 93), (5, 94, 190), (7, 191, 317), (5, 318, 416), (7, 417, 543), (5, 544, 637), (7, 638, 757), (5, 758, 858), (7, 859, 1008)]
#    Boxer2_8_1IdealData=[(7, 0, 117), (5, 118, 196), (7, 197, 333), (5, 334, 425), (7, 426, 554), (5, 555, 645), (7, 646, 773), (5, 774, 868), (7, 869, 995)]
#
#    Boxer2_11_1IdealData=[(7, 0, 157), (1, 158, 170), (7, 171, 178), (6, 179, 217), (7, 218, 359), (1, 360, 375), (7, 376, 380), (6, 381, 416), (7, 417, 571), (1, 572, 587), (7, 588, 592), (6, 593, 632), (7, 633, 783), (1, 784, 798), (7, 799, 803), (6, 804, 846), (7, 847, 990)]
#    Boxer2_11_2IdealData=[(7, 0, 139), (1, 140, 156), (7, 157, 177), (3, 179, 224), (7, 225, 645), (1, 646, 654), (7, 655, 674), (6, 675, 721), (7, 722, 865), (1, 866, 879), (7, 880, 898), (6, 899, 946), (7, 947, 1081), (1, 1082, 1095), (7, 1096, 1109), (6, 1110, 1156), (7, 1157, 1288)]
#    
#    Boxer3_1_1IdealData=[(7, 0, 135), (1, 136, 147), (7, 148, 203), (1, 204, 209), (7, 210, 272), (1, 273, 282), (7, 283, 336), (1, 337, 348), (7, 349, 504)]
#    Boxer3_1_2IdealData=[(7, 0, 206), (1, 207, 220), (7, 221, 311), (1, 312, 323), (7, 324, 408), (1, 409, 421), (7, 422, 503), (1, 504, 517), (7, 518, 644)]
#
#    Boxer3_3_1IdealData=[(7, 0, 115), (6, 116, 144), (7, 145, 200), (6, 201, 231), (7, 232, 293), (6, 294, 326), (7, 327, 384), (6, 385, 417), (7, 418, 554)]
#    Boxer3_3_2IdealData=[(7, 0, 146), (6, 147, 187), (7, 188, 296), (6, 297, 338), (7, 339, 430), (6, 431, 478), (7, 479, 565), (6, 566, 611), (7, 612, 761)]
#    
#    Boxer3_5_1IdealData=[(7, 0, 109), (3, 110, 156), (7, 157, 249), (3, 250, 295), (7, 296, 390), (3, 391, 436), (7, 437, 519), (3, 520, 566), (7, 567, 703)]
#    Boxer3_5_2IdealData=[(7, 0, 174), (3, 175, 234), (7, 235, 335), (3, 336, 383), (7, 384, 487), (3, 488, 537), (7, 538, 641), (3, 642, 705), (7, 706, 842)]
#
#    Boxer3_7_1IdealData=[(7, 0, 153), (2, 154, 186), (7, 187, 319), (2, 320, 361), (7, 362, 487), (2, 487, 526), (7, 527, 653), (2, 654, 696), (7, 697, 863)]
#    Boxer3_7_2IdealData=[(7, 0, 160), (2, 161, 211), (7, 212, 346), (2, 347, 404), (7, 405, 528), (2, 529, 586), (7, 587, 701), (2, 702, 754), (7, 755, 909)]
#
#    Boxer3_8_1IdealData=[(7, 0, 133), (5, 134, 199), (7, 200, 309), (5, 310, 380), (7, 381, 481), (5, 482, 556), (7, 557, 654), (5, 655, 727), (7, 728, 885)]
#    Boxer3_8_2IdealData=[(7, 0, 134), (5, 135, 230), (7, 231, 301), (5, 302, 420), (7, 421, 514), (5, 515, 617), (7, 618, 699), (5, 700, 795), (7, 796, 941)]
#
#    Boxer3_11_1IdealData=[(7, 0, 110), (1, 111, 116), (7, 117, 133), (6, 134, 162), (7, 163, 252), (1, 253, 259), (7, 260, 276), (6, 277, 304), (7, 305, 391), (1, 392, 400), (7, 401, 416), (6, 417, 443), (7, 444, 523), (1, 524, 530), (7, 531, 548), (6, 549, 578), (7, 579, 759)]
#    Boxer3_11_2IdealData=[(7, 0, 133), (1, 134, 149), (7, 150, 176), (6, 177, 217), (7, 219, 348), (1, 349, 368), (7, 369, 392), (6, 393, 437), (7, 438, 565), (1, 566, 579), (7, 580, 598), (6, 599, 644), (7, 645, 752), (1, 753, 773), (7, 774, 791), (6, 792, 835), (7, 836, 1029)]
#
#    



    #ml=[]
    #for i in xrange(1000):
    #    ml.append(random.randint(1,7))
    #t1 = timeit.Timer('fitnessutil.GetIndexesOfGroupsInList(ml)' ,  'from __main__ import ml ;import fitnessutil')
    #print t1.repeat(1,300)
    