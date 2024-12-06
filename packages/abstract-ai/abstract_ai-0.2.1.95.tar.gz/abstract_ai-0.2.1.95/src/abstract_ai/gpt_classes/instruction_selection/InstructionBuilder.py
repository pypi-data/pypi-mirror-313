from abstract_utilities import get_actual_number,eatAll
from abstract_utilities.type_utils import is_bool
def get_dict_from_instruction(instructions):
    new_instructions={}
    if instructions:
        count = 0
        if isinstance(instructions,str):
            new_instructions[f"additional_instructions_{count}"]={"instruction":instructions,"example":"","default":True}
        elif isinstance(instructions,list):
            for instruction in instructions:
                if isinstance(instruction,str):
                    new_instructions[f"additional_instructions_{count}"] = {"instruction":instruction,"example":"","default":True}
                    count +=1
                if isinstance(instruction,dict):
                    new_instruction = {"instruction":"","example":"","default":True}
                    new_instruction.update(instruction)
                    new_instructions[f"additional_instructions_{count}"] = new_instruction
                    count +=1
        elif isinstance(instructions,dict):
            for key,value in instructions.items():
                new_instruction = {"instruction":"","example":"","default":True}
                new_instruction.update(instructions[key])
                new_instructions[key] = new_instruction
    return new_instructions
class InstructionManager:
    def __init__(self,instructions=None,instruction_bools={})->None:
        instruction_bools = instruction_bools or {}
        self.default_instructions = {
                    "api_response": {
                        "instruction": "Place response to prompt here.",
                        "example": "This is the reply to your request.",
                        "default":True},
                    "additional_responses": {
                        "instruction": "Marking 'True' initiates a loop which continues to send the current chunk's prompt until the module returns a 'False' value.",
                        "example": "false",
                        "default":False},
                    "generate_title": {
                        "instruction": "Generate a short and concise title for this query, using underscores instead of spaces and avoiding special characters. The title should not exceed 200 characters to ensure compatibility with file systems.",
                        "example": "Short_Title_for_Query",
                        "default":True},
                    "database_query":{
                        "instruction": "the given database Schema,variables,values and function are provided in the prompt data; please derive the most appropriate inputs for a database query from the context and assertons of the request. place all inputs for the function within this respons key",
                        "example": {"query":"""SELECT dnc_data FROM dncdata WHERE dnc_data ->> 'Data_Subscriber_First_Name' = 'Karen';"""},
                        "default":False},
                    "notation": {
                        "instruction": "notation is a module end  functionality that allows the module, you, to to preserve relevant information or context for subsequent prompts; allowing for communication between modules throughout the query iterations. ",
                        "example": "Selecting additional responses due to insufficient completion tokens.",
                        "default":False},
                    "suggestions": {
                        "instruction": "This parameter allows the module to provide suggestions for improving efficiency in future prompt sequences.",
                        "example": "Consider batching queries to reduce server load",
                        "default":False},
                    "abort": {
                        "instruction": "If you cannot fulfill the request, respond with this value as 'True'. Leave a detailed reason as to why the query stream was aborted in 'suggestions'",
                        "example": "False",
                        "default":False},
                    "prompt_as_previous": {
                        "instruction": "This is a user-end declaration. If this is visible, the request portion of the prompt will change to include previous response data, if needed",
                        "example": "True",
                        "default":False},
                    "request_chunks": {
                        "instruction": "Request to prompt again the previous chunk data. If selected, the query will iterate once more with the previous data chunk included in the prompt.",
                        "example": "False",
                        "default":False},
                    "token_adjustment": {
                        "instruction": "Suggest percentage adjustments, between -100 up to 100, for the future token allotment. If it will provide better results to increase or decrease the future allotment, place a number.",
                        "example": "0",
                        "default":False},
                    }
        self.instructions = [[]]
        
        self.default_instructions.update(get_dict_from_instruction(instructions))
        for key,value in instruction_bools.items():
            self.default_instructions[key]['default'] = value
        self.update_instructions(0,**{key:self.default_instructions[key] for key in self.default_instructions if self.default_instructions[key].get('default')})
    def get_instructions(self,instruction_number:int=None)->dict:
        if len(self.instructions)==0:
            self.add_instructions()
        instruction_number = instruction_number or -1
        return self.instructions[instruction_number]
    def update_default_instructions(self,data):
        self.default_instructions.update(get_dict_from_instruction(data))
        self.update_instructions(0,**{key:self.default_instructions[key] for key in self.default_instructions if self.default_instructions[key].get('default')})
    def get_instructions_bools(self,parameters:dict)->dict:
        for parameter,value in parameters.items():
            parameters[parameter] = True if value else False
        return parameters
    
    def get_instructions_text_values(self,instruction_bools:dict,parameters:dict)->dict:
        parameter_text_values = {}
        for parameter,value in instruction_bools.items():
            if value:
                parameter_text_values[parameter] = self.default_instructions[parameter]['instruction'] if is_bool(parameters[parameter]) else  parameters[parameter]
        return parameter_text_values
    def get_instructions_text(self,instructions_js:dict)->dict:
        """
        Retrieves instructions for the conversation.

        Returns:
            None
        """
        instructions = ""
        example_format={}
        if instructions_js:
            instructions = "your response is expected to be in JSON format, while any boool responses are to be lowercase with no quotations surrounding their values, with the keys as follows:\n\n"
            i=0
            for key in instructions_js.keys():
                if key in self.default_instructions.keys():
                    instructions+=f'''{i}) {key} - """{eatAll(instructions_js[key],['"'])}"""\n'''
                    example_format[key]=self.default_instructions[key]['example']
                    i+=1
            instructions += '\nbelow is an example of the expected json dictionary response format, with the default inputs:\n' + str(example_format).replace("'",'"')
        return instructions
    def add_instructions(self,all_true:bool=False,**kwargs)->None:
        print('adding instructions')
        if len(self.instructions)==0:
            instruction_display,instruction_bools,instructions_text_values,instructions_text=self.get_instructions_values(all_true,**kwargs)
            last_instructions = {'instruction_display':instruction_display,'instructions_bools':instruction_bools,"instructions_text_values":instructions_text_values,"instructions_text":instructions_text,"text":instructions_text}
        else:
            last_instructions = self.instructions[-1]
        self.instructions.append(last_instructions)
        
    def get_instructions_values(self,all_true:bool= False,**kwargs)->(bool,dict,dict,str):
        parameters = {}
        for parameter in self.default_instructions.keys():
            value = kwargs.get(parameter,False) if all_true == False else True
            parameters[parameter]=value
        instruction_display=kwargs.get("instruction_display",True)    
        instruction_bools = self.get_instructions_bools(parameters)
        instructions_text_values= self.get_instructions_text_values(instruction_bools,parameters)
        instructions_text = self.get_instructions_text(instructions_js=instructions_text_values)
        return instruction_display,instruction_bools,instructions_text_values,instructions_text
    
    def update_instructions(self,instruction_number:int=0,**kwargs)->None:
        
        instruction_display,instruction_bools,instructions_text_values,instructions_text=self.get_instructions_values(**kwargs)
        self.instructions[instruction_number]={'instruction_display':instruction_display,'instructions_bools':instruction_bools,"instructions_text_values":instructions_text_values,"instructions_text":instructions_text,"text":instructions_text}
