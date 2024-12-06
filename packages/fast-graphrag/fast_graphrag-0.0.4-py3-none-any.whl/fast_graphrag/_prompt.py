"""Prompts."""

from typing import Any, Dict

PROMPTS: Dict[str, Any] = {}

## NEW
PROMPTS["entity_relationship_extraction"] = """You are a helpful assistant that helps a human analyst perform information discovery in the following domain.

# DOMAIN
{domain}

# GOAL
Given a document and a list of types, first, identify all present entities of those types and, then, all relationships among the identified entities.
Your goal is to highlight information that is relevant to the domain and the questions that may be asked on it.

Examples of possible questions:
{example_queries}

# STEPS
1. Identify all entities of the given types. Make sure to extract all and only the entities that are of one of the given types, ignore the others. Use singular names and split compound concepts when necessary (for example, from the sentence "they are movie and theater directors", you should extract the entities "movie director" and "theater director").
2. Identify all relationships between the entities found in step 1. Clearly resolve pronouns to their specific names to maintain clarity.
3. Double check that each entity identified in step 1 appears in at least one relationship. If not, add the missing relationships.

# EXAMPLE DATA
Example types: [location, organization, person, communication]
Example document: Radio City: Radio City is India's first private FM radio station and was started on 3 July 2001. It plays Hindi, English and regional songs. Radio City recently forayed into New Media in May 2008 with the launch of a music portal - PlanetRadiocity.com that offers music related news, videos, songs, and other music-related features."

Output:
{{
	"entities": [
	{{"name": "Radio City", "type": "organization", "desc": "Radio City is India's first private FM radio station."}},
	{{"name": "India", "type": "location", "desc": "The country of India."}},
	{{"name": "FM radio station", "type": "communication", "desc": "A radio station that broadcasts using frequency modulation."}},
	{{"name": "English", "type": "communication", "desc": "The English language."}},
	{{"name": "Hindi", "type": "communication", "desc": "The Hindi language."}},
	{{"name": "New Media", "type": "communication", "desc": "New Media is a term for all forms of media that are digital and/or interactive."}},
	{{"name": "PlanetRadiocity.com", "type": "organization", "desc": "PlanetRadiocity.com is an online music portal."}},
	{{"name": "music portal", "type": "communication", "desc": "A website that offers music related information."}},
	{{"name": "news", "type": "communication", "desc": "The concept of news."}},
	{{"name": "video", "type": "communication", "desc": "The concept of a video."}},
	{{"name": "song", "type": "communication", "desc": "The concept of a song."}}
	],
	"relationships": [
	{{"source": "Radio City", "target": "India", "desc": "Radio City is located in India."}},
	{{"source": "Radio City", "target": "FM radio station", "desc": "Radio City is a private FM radio station started on 3 July 2001."}},
	{{"source": "Radio City", "target": "English", "desc": "Radio City broadcasts English songs."}},
	{{"source": "Radio City", "target": "Hindi", "desc": "Radio City broadcasts songs in the Hindi language."}},
	{{"source": "Radio City", "target": "PlanetRadiocity.com", "desc": "Radio City launched PlanetRadiocity.com in May 2008."}},
	{{"source": "PlanetRadiocity.com", "target": "music portal", "desc": "PlanetRadiocity.com is a music portal that offers music related news, videos and more."}},
	{{"source": "PlanetRadiocity.com", "target": "video", "desc": "PlanetRadiocity.com offers music related videos."}}
	],
	"other_relationships": [
	{{"source": "Radio City", "target": "New Media", "desc": "Radio City forayed into New Media in May 2008."}},
	{{"source": "PlanetRadiocity.com", "target": "news", "desc": "PlanetRadiocity.com offers music related news."}},
	{{"source": "PlanetRadiocity.com", "target": "song", "desc": "PlanetRadiocity.com offers songs."}}
	]
}}

# REAL DATA
Types: {entity_types}
Document: {input_text}

Output:
"""

PROMPTS["entity_relationship_continue_extraction"] = "MANY entities were missed in the last extraction.  Add them below using the same format:"

PROMPTS["entity_relationship_gleaning_done_extraction"] = "Retrospectively check if all entities have been correctly identified: answer done if so, or continue if there are still entities that need to be added."

PROMPTS["entity_extraction_query"] = """Given the query below, your task is to extract all entities relevant to perform information retrieval to produce an answer.

-Example 1-
Query: Who directed the film that was shot in or around Leland, North Carolina in 1986?
Ouput: {{"named": ["Leland", "North Carolina", "1986"], "generic": ["film director"]}}

-Example 2-
Query: What relationship does Fred Gehrke have to the 23rd overall pick in the 2010 Major League Baseball Draft?
Ouput: {{"named": ["Fred Gehrke", "2010 Major League Baseball Draft"], "generic": ["23rd baseball draft pick"]}}

# INPUT
Query: {query}
Output:
"""



PROMPTS[
	"summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given the current description, summarize it in a shorter but comprehensive description. Make sure to include all important information.
If the provided description is contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

Current description:
{description}

Updated description:
"""


PROMPTS[
	"edges_group_similar"
] = """You are a helpful assistant responsible for maintaining a list of facts describing the relations between two entities so that information is not redundant.
Given a list of ids and facts, identify any facts that should be grouped together as they contain similar or duplicated information and provide a new summarized description for the group.

# EXAMPLE
Facts (id, description):
0, Mark is the dad of Luke
1, Luke loves Mark
2, Mark is always ready to help Luke
3, Mark is the father of Luke
4, Mark loves Luke very much

Ouput:
{{
	grouped_facts: [
	{{
		'ids': [0, 3],
		'description': 'Mark is the father of Luke'
	}},
	{{
		'ids': [1, 4],
		'description': 'Mark and Luke love each other very much'
	}}
	]
}}

# INPUT:
Facts:
{edge_list}

Ouput:
"""

PROMPTS["generate_response_query_with_references"] = """You are a helpful assistant analyzing the given input data to provide an helpful response to the user query.

# INPUT DATA
{context}

# USER QUERY
{query}

# INSTRUCTIONS
Your goal is to provide a response to the user query using the relevant information in the input data:
- the "Entities" and "Relationships" tables contain high-level information. Use these tables to identify the most important entities and relationships to respond to the query.
- the "Sources" list contains raw text sources to help answer the query. It may contain noisy data, so pay attention when analyzing it.

Follow these steps:
1. Read and understand the user query.
2. Look at the "Entities" and "Relationships" tables to get a general sense of the data and understand which information is the most relevant to answer the query.
3. Carefully analyze all the "Sources" to get more detailed information. Information could be scattered across several sources, use the identified relevant entities and relationships to guide yourself through the analysis of the sources.
4. While you write the response, you must include inline references to the all the sources you are using by appending `[<source_id>]` at the end of each sentence, where `source_id` is the corresponding source ID from the "Sources" list.
5. Write the response to the user query - which must include the inline references - based on the information you have gathered. Be very concise and answer the user query directly. If the response cannot be inferred from the input data, just say no relevant information was found. Do not make anything up or add unrelevant information.

Answer:
"""

PROMPTS["generate_response_query_no_references"] = """You are a helpful assistant analyzing the given input data to provide an helpful response to the user query.

# INPUT DATA
{context}

# USER QUERY
{query}

# INSTRUCTIONS
Your goal is to provide a response to the user query using the relevant information in the input data:
- the "Entities" and "Relationships" tables contain high-level information. Use these tables to identify the most important entities and relationships to respond to the query.
- the "Sources" list contains raw text sources to help answer the query. It may contain noisy data, so pay attention when analyzing it.

Follow these steps:
1. Read and understand the user query.
2. Look at the "Entities" and "Relationships" tables to get a general sense of the data and understand which information is the most relevant to answer the query.
3. Carefully analyze all the "Sources" to get more detailed information. Information could be scattered across several sources, use the identified relevant entities and relationships to guide yourself through the analysis of the sources.
4. Write the response to the user query based on the information you have gathered. Be very concise and answer the user query directly. If the response cannot be inferred from the input data, just say no relevant information was found. Do not make anything up or add unrelevant information.

Answer:
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."
