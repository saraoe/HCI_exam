<p align="center">
![My image](https://github.com/saraoe/HCI_exam/blob/main/fig/logo-removebg.png)

# Human Computer Interaction Exam

Exam project for Human Computer Interaction (HCI) by Emil Jessen &amp; Sara Østergaard.
</p>

## Abstract
The progression in the field of NLP calls for data sharing, however, GDPR legislation restricts data distribution as much data includes identifiable information. Anonymization of documents may make data comply to legislation, and thus shareable. Manual anonymization of documents remains a cumbersome feat, partially due to the cognitive constraint of limited attention given repetitive tasks. Developments in language models provide a method for automatic annotation, however, steps toward making a widely available anonymization tool that satisfies formal legislation are needed.
We propose our newly developed tool _HIanonymize_ to improve the process of anonymizing text documents. It relies on hybrid intelligence to provide an optimal solution for anonymizing unstructured texts by capitalizing on both the swiftness of AI and the flexibility of humans. The tool takes the form of a web app, supporting usability while attempting to maintain high functionality.
Apart from presenting our product and the design of the product, we also discuss potential design limitations of the tool pertaining to large quantities of text and review future prospects for development.

## Project Organization
The organization of the project is as follows:

```
├── README.md                  <- The top-level README for this project.
├── example_data               <- documents for running example   
│   └── .txt
├── descriptions
│   └── ...    
├── src   
│   ├── text_anonymization.py                 
│   └── util.py
├──  requirement.txt           <- A requirements file of the required packages.
└──  app.py                    <- streamlit app
```

## Run app
To run the app clone the repository and run the following
```
pip install -r requirements.txt
```

```
streamlit run app.py
```

You can use you own files to test the app or use the documents in the folder ```example_data```.
