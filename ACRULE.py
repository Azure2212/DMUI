import math

class ACRULE:
    def __init__(self, X, Y):
        # for Rule: X -> Y
        self.antecedent = X                # X
        self.consequent = Y                 # Y
        self.antecedentSUP = 0.0            # SUP(X)
        self.antecedentNConsequentSUP = 0.0 # SUP(XY)
        self.confidence = 0.0               # SUP(XY)/SUP(X)
        self.confidencePurity = 0.0               # confidence*(1-entropy)
  
    def toString(self):
        return f"{self.antecedent} ===> {self.consequent} (supportX = {self.antecedentSUP}, supportXY = {self.antecedentNConsequentSUP}, confidence = {round(self.confidence,2)}, confidencePurity = {round(self.confidencePurity,2)})"

    def fromJson(self, data):
        clean = {k.strip(): v for k, v in data.items()}

        self.antecedent = clean.get("antecedent", [])
        self.consequent = clean.get("consequent", None)
        self.antecedentSUP = clean.get("antecedentSUP", 0.0)
        self.antecedentNConsequentSUP = clean.get("antecedentNConsequentSUP", 0.0)
        self.confidence = clean.get("confidence", 0.0)
        self.confidencePurity = clean.get("confidencePurity", 0.0)

        return self
        
def classifier1(rules, mapping, subClasses, new_sample):
    score_vector = {}
    encoded_sample = {}

    for col, val in new_sample.items():
        new_sample
        encoded_sample[col] = mapping.get(col, {}).get(val, 0)
    values_list = list(encoded_sample.values())
    #print(values_list)
    matchingRules = [rule for rule in rules if all(item in values_list for item in rule.antecedent)]
    # for r in matchingRules:
    #     print(r.toString())
    if len(matchingRules) == 0:
        return '404', "No Result for you symptoms"
    for subClass in subClasses:
        ruleWithConsequentIsSubClass = [rule for rule in matchingRules if rule.consequent == subClass]
        
        AvgWeight = 0.0
        for rule in ruleWithConsequentIsSubClass:
            w = rule.confidencePurity * (math.log(1+rule.antecedentSUP)/ math.log(len(subClasses)))
            AvgWeight += w
        #AvgWeight = AvgWeight / len(ruleWithConsequentIsSubClass)
        
        s_k = 0.9 * AvgWeight + 0.1 * (len(ruleWithConsequentIsSubClass)/(len(matchingRules)+1e-8))
        score_vector[subClass] = s_k
        
    max_value = max(score_vector.values())  # find maximum value
    predictedClass = [k for k, v in score_vector.items() if v == max_value]  # find all keys with that value
    #print(score_vector)
    #print(predictedClass[0])
    
    class_map = {"100": "Don't have high risk", "101": "have high risk"}

    conf_acc = score_vector[predictedClass[0]] / sum(score_vector.values())

    reason = f"With your input symptoms our system's prediction ensure {round(conf_acc*100,2)}% you {class_map[predictedClass[0]]}\n"
    reason += f"Based on 70,000 previous patient There {len(matchingRules)} rules on {len(rules)} fit with your symptoms\n"
    reason += f"With the number of rules implicating high risk = {len([rule for rule in matchingRules if rule.consequent == '101'])}\n"
    reason += f"With the number of rules implicating non-high risk = {len([rule for rule in matchingRules if rule.consequent == '100'])}"

    return predictedClass[0], reason