import torch

def verify_metrics(gt, pred, num_classes):
    # Compute the predicted class indices
    # pred_classes = [torch.argmax(pred, dim=1)]
    pred_classes = pred
    
    # Compute the ground truth class indices
    # gt_classes = torch.argmax(gt, dim=1)
    gt_classes = gt
    
    # Accuracy
    accuracy = torch.mean((pred_classes == gt_classes).float()).item()
    
    # Calculate F1 score for each class
    def calculate_f1_score(gt_classes, pred_classes, num_classes):
        f1_scores = []
        
        for i in range(num_classes):
            # True Positives (TP), False Positives (FP), False Negatives (FN)
            tp = torch.sum((pred_classes == i) & (gt_classes == i)).float()
            fp = torch.sum((pred_classes == i) & (gt_classes != i)).float()
            fn = torch.sum((pred_classes != i) & (gt_classes == i)).float()
            
            # Precision and Recall
            precision = tp / (tp + fp + 1e-8)  # Add small constant to avoid division by zero
            recall = tp / (tp + fn + 1e-8)     # Add small constant to avoid division by zero
            
            # F1 Score
            f1 = 2 * (precision * recall) / (precision + recall + 1e-8)  # Add small constant to avoid division by zero
            f1_scores.append(f1)
        
        # Average F1 Score across all classes
        avg_f1_score = torch.mean(torch.stack(f1_scores))
        
        return avg_f1_score
    
    # Compute F1 score
    f1 = calculate_f1_score(gt_classes, pred_classes, num_classes)
    
    return accuracy, f1.item()

# Example tensors
num_classes = 9  # Adjust this to match your number of classes
gt_action = torch.tensor([0, 1, 0, 0, 3, 1, 1, 1, 3, 0, 1, 0, 3, 0, 0, 1, 0, 1, 0, 2, 0, 3, 7, 1,
                           1, 1, 0, 2, 1, 1, 1, 3, 1, 0, 3, 0, 0, 0, 0, 1, 1, 1, 3, 2, 1, 3, 0, 0,
                           4, 2, 1, 2, 3, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 3,
                           1, 1, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 0, 1, 2, 0, 0, 3, 2, 1,
                           3, 0, 2, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
                           3, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 0, 0, 1, 3,
                           0, 3, 1, 2, 1, 4, 3, 0, 3, 1, 1, 0, 3, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0,
                           1, 0, 0, 1, 0, 4, 0, 0, 4, 1, 1, 0, 3, 1, 1, 1, 0, 3, 1, 0, 1, 0, 2, 3,
                           1, 3, 2, 0, 0, 0, 1, 1, 0, 1, 7, 0, 1, 0, 1, 3, 0, 0, 2, 0, 0, 0, 0, 1,
                           0, 1, 0, 3, 1, 1, 0, 0, 3, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1,
                           0, 0, 0, 3, 0, 1, 0, 1, 1, 0, 1, 1, 3, 1, 0, 0], dtype=torch.long).cuda()
pred_action = torch.tensor([8, 1, 8, 8, 8, 3, 8, 8, 2, 8, 3, 8, 1, 8, 8, 1, 3, 8, 8, 8, 8, 3, 8, 8,
                             8, 3, 8, 8, 8, 3, 6, 1, 3, 8, 8, 8, 8, 8, 8, 8, 3, 8, 8, 3, 8, 1, 8, 8,
                             8, 3, 8, 8, 1, 3, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 3, 8, 3, 3, 8, 8, 1, 1,
                             8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 3, 8, 8, 3, 8, 8, 8, 8, 8, 6, 8, 8, 3, 8,
                             2, 8, 8, 8, 8, 8, 8, 8, 3, 3, 8, 8, 8, 8, 8, 8, 3, 8, 8, 3, 8, 8, 1, 8,
                             8, 8, 8, 8, 8, 3, 3, 3, 3, 8, 8, 6, 8, 8, 8, 8, 3, 3, 8, 3, 8, 8, 3, 8,
                             8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                             3, 8, 3, 3, 8, 8, 8, 3, 8, 8, 8, 8, 8, 3, 8, 3, 6, 8, 3, 8, 8, 8, 6, 8,
                             3, 3, 1, 6, 6, 8, 8, 6, 6, 8, 6, 8, 3, 8, 8, 8, 8, 6, 8, 8, 8, 3, 8, 8,
                             8, 8, 3, 8, 8, 6, 8, 8, 2, 8, 8, 3, 8, 8, 3, 8, 3, 8, 8, 8, 8, 8, 8, 8,
                             3, 6, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 3, 3, 8, 8], dtype=torch.long).cuda()

accuracy, f1 = verify_metrics(gt_action, pred_action, num_classes)
print(f"Accuracy: {accuracy}, F1 Score: {f1}")
