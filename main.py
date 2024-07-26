import os
import re

def get_files_from_folder(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def get_max_existing_number(prefix_ydd, prefix_ytd, folder_path, ytd_suffix):
    files = get_files_from_folder(folder_path)
    max_number_ydd = -1
    max_number_ytd = -1

    pattern_ydd = re.compile(rf'{prefix_ydd}_(\d{{3}})_(u|r)\.ydd')
    pattern_ytd = re.compile(rf'{prefix_ytd}_(\d{{3}})_[a-z]{ytd_suffix}\.ytd')

    for file in files:
        match_ydd = pattern_ydd.match(file)
        if match_ydd:
            number = int(match_ydd.group(1))
            max_number_ydd = max(max_number_ydd, number)

        match_ytd = pattern_ytd.match(file)
        if match_ytd:
            number = int(match_ytd.group(1))
            max_number_ytd = max(max_number_ytd, number)

    return max(max_number_ydd, max_number_ytd)

def rename_files_with_prefix(folder_path, prefix_ydd, prefix_ytd, start_number, ytd_suffix, ydd_suffix):
    files = get_files_from_folder(folder_path)
    
    ydd_renamed = False
    for file in files:
        if file.endswith('.ydd') and prefix_ydd in file:
            new_name_ydd = f'{prefix_ydd}_{start_number:03d}_{ydd_suffix}.ydd'
            os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name_ydd))
            ydd_renamed = True
            break

    if ydd_renamed:
        letter = 'a'
        for file in files:
            if file.endswith('.ytd') and prefix_ytd in file:
                new_name_ytd = f'{prefix_ytd}_{start_number:03d}_{letter}{ytd_suffix}.ytd'
                os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name_ytd))
                letter = chr(ord(letter) + 1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    folder_path = r'PATH HERE'
    status_message = '[Status] Waiting...'
    
    clear_screen()

    while True:
        print(status_message)
        print("Commands:")
        print("  b <number> - Bottom (e.g., b 002)")
        print("  t <number> - Top (e.g., t 002)")
        print("  h <number> - Hair (e.g., h 002)")
        print("  x <number> - Hand (e.g., x 002)")
        print("  s <number> - Shoes (e.g., s 002)")
        print("  a <number> - Accessories (e.g., a 002)")
        print()
        command = input("[CMD] : ").strip()

        status_message = '[Status] Waiting...'
        
        match = re.match(r'(b|t|h|x|s|a) (\d{3})', command, re.IGNORECASE)
        if match:
            operation = match.group(1).lower()
            new_number = match.group(2)

            prefixes = {
                'b': ('lowr', 'lowr_diff', '_uni', 'r'),
                't': ('jbib', 'jbib_diff', '_uni', 'u'),
                'h': ('hair', 'hair_diff', '_uni', 'u'),
                'x': ('hand', 'hand_diff', '_uni', 'u'),
                's': ('feet', 'feet_diff', '_uni', 'u'),
                'a': ('accs', 'accs_diff', '_uni', 'u')
            }

            if operation in prefixes:
                prefix_ydd, prefix_ytd, ytd_suffix, ydd_suffix = prefixes[operation]

                try:
                    if new_number == '000':
                        start_number = 0
                    else:
                        max_existing_number = get_max_existing_number(prefix_ydd, prefix_ytd, folder_path, ytd_suffix)
                        start_number = int(new_number)
                    
                    rename_files_with_prefix(folder_path, prefix_ydd, prefix_ytd, start_number, ytd_suffix, ydd_suffix)
                    status_message = '[Status] Completed'
                except Exception as e:
                    status_message = '[Status] Error'
                    print(f"An error occurred: {e}")
            else:
                status_message = '[Status] Error'
        else:
            status_message = '[Status] Error'

        clear_screen()

if __name__ == "__main__":
    main()
