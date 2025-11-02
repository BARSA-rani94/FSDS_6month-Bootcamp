import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset=pd.read_csv(r"C:\Users\HP\Downloads\New folder\Restaurant_Reviews.tsv",delimiter='\t',quoting=3)

# Adding Duplicate rows
d2=pd.concat([dataset,dataset],ignore_index=True)
import re  
import nltk    # re--regular expression for removing . , ! ' etc
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpus=[]

for i in range(0,2000):
    review=re.sub('[^a-zA-Z]',' ',d2['Review'][i])
    review=review.lower()
    review=review.split()
    ps=PorterStemmer()
    review=[ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review=' '.join(review)
    corpus.append(review)
    
# Creating the BOW model
from sklearn.feature_extraction.text import TfidfVectorizer
cv=TfidfVectorizer()
x=cv.fit_transform(corpus).toarray()
y=d2.iloc[:,1].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=0)

from sklearn.tree import DecisionTreeClassifier
classifier=DecisionTreeClassifier(random_state=0)
classifier.fit(x_train,y_train)

y_pred=classifier.predict(x_test)
 
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred)
print(cm)

from sklearn.metrics import accuracy_score
ac=accuracy_score(y_test,y_pred)
ac

bias=classifier.score(x_train,y_train)
print(bias)

variance=classifier.score(x_test,y_test)
print(variance)


# Save the model
import pickle
with open("restaurant_review.pkl",'wb') as model_file:
    pickle.dump(classifier,model_file)
with open("vectorizer.pkl",'wb') as vec_file:
    pickle.dump(cv,vec_file)
