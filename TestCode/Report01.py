import re 

def parentheses_repression(text):
    return bool(re.search('^\(([\(\)]{0,99998})\)$',text));

if __name__ == "__main__":
    print(parentheses("()()"),"\n")
    print(parentheses("(())()"),"\n")
    print(parentheses(")()("),"\n")
    print(parentheses("(()("),"\n")



    
