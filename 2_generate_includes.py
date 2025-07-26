import re

def extract_regex_from_js(js_code):
    pattern1 = r"(?<!//)(?<!/\*)BypassedByBloggerPemula\('([^']+)',"
    matches1 = re.findall(pattern1, js_code)
    matches1 = [match.strip('/') for match in matches1]

    pattern1b = r'(?<!//)BypassedByBloggerPemula\(/\s*([a-zA-Z0-9.-]+)\s*/,'
    matches1b = re.findall(pattern1b, js_code)

    pattern1c = r'(?<!//)BypassedByBloggerPemula\((/[^/]*?/,)'
    matches1c = re.findall(pattern1c, js_code)
    matches1c = [match.strip("/',") for match in matches1c]

    pattern2 = r"(?<!//)BloggerPemula\('([^']+)',"
    matches2 = re.findall(pattern2, js_code)

    pattern3 = r"(?<!//)RemoveBp\('([^']+)',"
    matches3 = re.findall(pattern3, js_code)

    pattern4 = r'(?<!//)case \'(.*?)\':'
    matches4 = re.findall(pattern4, js_code)

    pattern5 = r"h\.href\.includes\('(.*?)'\)"
    matches5 = re.findall(pattern5, js_code)

    allmatches = matches1+matches1b+matches1c+matches2+matches3+matches4+matches5

    # remove duplicates
    allmatches = list(dict.fromkeys(allmatches))

    return allmatches

def write_list_of_strings_to_file(filename, lines):
    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')
    if len(lines) > 0:
        print(f"OK: Generated {filename}")

def generate_include_lines(regex_list):
    include_rules = []
    match_rules = []
    include_and_match_lines = []

    for regex in regex_list:

        #Use @include for more complex regex
        if any(char in regex for char in ['|', '(', ')', '*']):
            regex = '(' + regex + ')'
            include_rule = r"/^(https?:\/\/)(.+)?" + regex + r"(\/.*)/"
            include_rule = include_rule.replace(r"\.*)(\/.*)/", r"\.*)/")  # clean excess in the regex
            include_rules.append(include_rule)
            include_line = "// @include " + include_rule
            include_and_match_lines.append(include_line)

        #Use @match for simpler regex
        else:
            match_rule = '*://*.' + regex + '/*'
            match_rules.append(match_rule)
            match_line =  '// @match ' + match_rule
            include_and_match_lines.append(match_line)

    #Output results to txt files
    write_list_of_strings_to_file('supported_sites.txt', regex_list)
    write_list_of_strings_to_file('match_rules.txt', match_rules)
    write_list_of_strings_to_file('include_rules.txt', include_rules)
    write_list_of_strings_to_file('includes.txt', include_and_match_lines)


def main():

    # Clear the content of the files include_rules.txt, match_rules.txt, supported_sites.txt, includes.txt
    write_list_of_strings_to_file('supported_sites.txt', [])
    write_list_of_strings_to_file('match_rules.txt', [])
    write_list_of_strings_to_file('include_rules.txt', [])
    write_list_of_strings_to_file('includes.txt', [])



    file_path = 'untouched_Bypass_All_Shortlinks_patched.user.js'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            js_code = file.read()

            regex_strings = extract_regex_from_js(js_code)

            # remove duplicates from regex_strings
            regex_strings = list(dict.fromkeys(regex_strings))

            # remove short domains (errors)
            regex_strings = [s for s in regex_strings if "." in s and len(s) >= 5]

            # remove domains with blocked words (to avoid people worrying)
            blocked_words_for_includes = [
                "google", #drive/docs autoDL, bypass redirects, captchas
                "youtube", #redirecting shorts
                "twitter.com", #bypass redirects
                "facebook.com", #bypass redirects
                "tiktok.com", #bypass redirects
                "vk.com" #bypass redirects
            ]
            regex_strings = [s for s in regex_strings if not any(word in s for word in blocked_words_for_includes)]

            generate_include_lines(regex_strings)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
