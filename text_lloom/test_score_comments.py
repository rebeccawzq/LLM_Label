import pandas as pd
import asyncio
from concept import Concept
# from llm import multi_query_gpt_wrapper, calc_cost_by_tokens  # Assuming these exist as per your structure

# Import the necessary functions from the existing module
from concept_induction import score_concepts

# Create a mock dataset with comments to test
# data = {
#     "doc_id": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
#     "text": [
#         "Socioeconomic integration (via busing or school redistricting) is a good starting point.\nIntegrating schools better distributes the 'burden' those in poverty face and typically grants them access to better resources.\nThe US has higher poverty rates, weaker safety nets, and tremendous income inequality.",
#         "Just increasing funding for public schools obviously hasn't really been working as intended.  Per student costs differ all over the country yet there is not a correlation between test scores and funding in this respect.  Many schools continue to receive high levels of public funding with zero results.",
#         "There really is no U.S. system. There are 50 state systems and a federal bureaucracy that helps push out standards and so forth. Nationalizing this is a non-starter. So the question is, is there anything the federal government can incentivize? I'd argue we've collectively placed too much emphasis on pushing kids from high school to college and not enough on early childhood education. Politically it's attractive to say 'see, look how many kids got into college' even though many of them require significant remedial help as compared with the long term investment of expanding pre-k, Longer school years and so forth. ",
#         "Universal Pre-K, more choices for students in terms of subjects,  shorter summer holiday, higher wages for teachers, no multiple choice tests, not allowing creationism being taught alongside evolution, less students",
#         "This is kind of what I'm talking about.  I went to religious private school. I also got sex education and learned about evolution on a planet billions of years old.  Your assumptions are stereotypes and not universal, and the reactionary idea that religious education equals backwards thinking in all areas of learning simply isn't reality. ",
#         "Also, granted I only work in a k-8 district, we don't even use text books in our district. We're on a 1:1 program for laptops and use a variety of web sites for our material. ",
#         "Nothing can ever completely stop it, however if all kids from Alabama are taught that the Civil War was only about states rights and then move to Florida where people tell them the other side then it is easy to stumble across the truth, if it is an entire nation of lies how many will ever know the truth? No one is right all the time and no one has all the answers.  The Europeans conquered much of the world because of gunpowder which came not from Europe  but from china.  Columbus didn't discover America with the crowns backing, Lief Ericsson did it (presumably ) on his own blood and guts and sweat.  GMO's haven't been proven unsafe regardless of what some pockets of people claim. We will always have propaganda and altering opinions but that is probably a better thing than everyone believing the same lie. ",
#         "Who defines a bad student? Where do they go? All citizens have a right to an education, and repeat offenders already get put into alternative schools.",
#         "School days need to go from 8 AM to 5 PM. Extra teachers are needed to get this schedule to work. BUT, as a trade-off, no homework should be assigned. Use extra periods in classes for recitation and in-class work.",
#         "kids are smarter than we give them credit; its a habit of getting older. kids need creative, free play. you need flexible, reflexive, spontaneous teachers to accompany that. we've seen the effect standardization has on education, and its quite disgusting. ",
#         "I know a number of researchers who would gladly career change into the teaching profession, even knowing the pay drop, due to personal and idealistic reasons but almost none of them are pursuing it because the hoops you gotta jump through are just asinine.",
#         "$50-60k, but you're 'supposed'to be working ~6 hour days. When I was in school, it ran from 7 AM to 3:30 PM. Also, teachers have to prepare for their classes outside of those hours and grade homework/tests. How are you possibly getting six hour days?",
#         "In addition to Sweden, Finland, which is widely reputed to have the best schools in the world, operates on a system of complete school choice that amounts to making every school a charter school. And then, of course, there's the US system of higher education, which is not only universally considered to be the best in the wrold, but more privatized than any other by orders of magnitude."
#         "Encourage actual parental involvement, especially among the working poor.  I would like to see something along the lines of paying lower income parents to come to school at the end of the school day and work with their children on homework. "
#     ]
# }

# Load the dataset into a DataFrame
df = pd.read_excel('education.xlsx')
df = df.rename(columns={'id': 'doc_id'})

# Assuming you have already built concepts and have them as a dictionary of concept_id -> Concept objects
concepts = {
    "c1": Concept(name="School District Integration",
                  prompt="Does the comment mention anything about School District Integration?",
                  example_ids=["dsbt2tb"],
                  active=True),

    "c2": Concept(name="Invest $ in students",
                  prompt="Does the comment mention anything about Investing in students (e.g., funding, resources)?",
                  example_ids=["dseaozz"],
                  active=True),

    "c3": Concept(name="Decentralized Education Systems",
                  prompt="Does the comment mention anything about Decentralized Education Systems?",
                  example_ids=["dsbtzsn"],
                  active=True),

    "c4": Concept(name="Invest in pre-k",
                  prompt="Does the comment mention anything about Investing in pre-K education?",
                  example_ids=["dsdbi3x"],
                  active=True),

    "c5": Concept(name="Privatization",
                  prompt="Does the comment mention anything about Privatization (e.g., vouchers, private schools)?",
                  example_ids=["dsd5sxm"],
                  active=True),

    "c6": Concept(name="Adjust school resources (within and for)",
                  prompt="Does the comment mention anything about Adjusting school resources within and for schools?",
                  example_ids=["dsddsg3"],
                  active=True),

    "c7": Concept(name="Political bias",
                  prompt="Does the comment mention anything about Political bias in education?",
                  example_ids=["dsbzgmm"],
                  active=True),

    "c8": Concept(name="School power, to give teachers more agency (problematic students)",
                  prompt="Does the comment mention anything about giving schools or teachers more power to handle problematic students?",
                  example_ids=["dsdmsj8"],
                  active=True),

    "c9": Concept(name="Adjust school scheduling/timing",
                  prompt="Does the comment mention anything about Adjusting school scheduling or timing?",
                  example_ids=["dsc3xbs"],
                  active=True),

    "c10": Concept(name="Adjust student assessment metrics (eg standardized testing)",
                   prompt="Does the comment mention anything about Adjusting student assessment metrics like standardized testing?",
                   example_ids=["dsc4jlp"],
                   active=True),

    "c11": Concept(name="Professional development for teachers",
                   prompt="Does the comment mention anything about Professional development for teachers?",
                   example_ids=["dsd1mc6"],
                   active=True),

    "c12": Concept(name="Teacher compensation",
                   prompt="Does the comment mention anything about Teacher compensation?",
                   example_ids=["dsd50b8"],
                   active=True),

    "c13": Concept(name="Overhaul curriculum",
                   prompt="Does the comment mention anything about Overhauling curriculum or alternatives to public schools (e.g., charter schools, trade schools)?",
                   example_ids=["dsc8tbc"],
                   active=True),

    "c14": Concept(name="Promote parental involvement (Homeschooling)",
                   prompt="Does the comment mention anything about Promoting parental involvement or homeschooling?",
                   example_ids=["dscaxn8"],
               active=True)
}


# Set the column names for document and document ID
text_col = "text"
doc_id_col = "doc_id"


def get_in_concept_set(score_df, concept_id, threshold=0.5):
    subset = score_df[score_df["concept_id"] == concept_id]
    in_concept_docs = subset[subset["score"] >= threshold]["doc_id"].unique()
    return set(in_concept_docs)


def jaccard_similarity(setA, setB):
    intersection = len(setA.intersection(setB))
    union = len(setA.union(setB))
    if union == 0:
        return 1.0  # If both sets are empty, they are identical
    return intersection / union




# Function to run the test
async def main():
    # Score the comments
    runs_results = {}

    for i in range(5):
        score_df_run, summaries = await score_concepts(df, text_col=text_col, doc_id_col=doc_id_col, concepts=concepts,
                                        model_name="gpt-3.5-turbo", get_highlights=True, batch_size=2)

        runs_results[f'{i}th_run'] = score_df_run




    # Display the results
    # print(score_df.columns)
    # print('*' * 50)
    # for summary in summaries:
    #     print(summary)
    # score_df.to_excel('score_concepts.xlsx')


# Run the test
if __name__ == "__main__":
    asyncio.run(main())
