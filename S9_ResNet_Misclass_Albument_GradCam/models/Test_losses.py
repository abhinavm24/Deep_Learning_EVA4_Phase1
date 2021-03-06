from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from tqdm import tqdm

# # class for Calculating and storing testing losses and testing accuracies of model for each epoch ## 
class Test_loss:

       def test_loss_calc(self,model, device, test_loader, total_epoch, current_epoch):
           self.model        = model
           self.device       = device
           self.test_loader  = test_loader
           self.total_epoch  = total_epoch
           self.current_epoch= current_epoch   
       
           model.eval()
           
           correct        = 0 
           total          = 0              
           test_loss      = 0
           test_accuracy  = 0 
           test_losses    = []
           test_acc       = []
           predicted_class= []
           actual_class   = []
           wrong_predict  = []
           count_wrong    = 0   
           
           with torch.no_grad():               # For test data, we won't do backprop, hence no need to capture gradients
                for images,labels in test_loader:
 
                    images,labels    = images.to(device),labels.to(device)
                    labels_pred      = model(images)
                    test_loss        += F.nll_loss(labels_pred, labels, reduction = 'sum').item()                        
                    labels_pred_max  = labels_pred.argmax(dim =1, keepdim = True)
                    correct          += labels_pred_max.eq(labels.view_as(labels_pred_max)).sum().item()
                    total            += labels.size(0) 
              
                    if count_wrong   < 26 and current_epoch == (total_epoch - 1):  # Capturing 26 wrongly predicted images for last epoch
                       for i in range(len(labels_pred_max)):                       # with its predicted and actual class
                            if labels_pred_max[i] != labels[i]:
                                   wrong_predict.append(images[i])
                                   predicted_class.append(labels_pred_max[i].item())
                                   actual_class.append(labels[i].item())
                                   count_wrong += 1
                
                test_loss   /= total  # Calculating overall test loss for the epoch
                test_losses.append(test_loss)    
                                  
                test_accuracy =  (correct/total)* 100
                test_acc.append(test_accuracy)             
               
                print('\nTest set: Average loss: {:.4f}, Test Accuracy: {:.2f}\n' .format(test_loss, test_accuracy))

           return test_losses, test_acc, wrong_predict, predicted_class, actual_class
