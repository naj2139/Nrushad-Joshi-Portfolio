#include<iostream>
#include<cstring>
#include<array>

using namespace std;

#define ALPHABET_LENGTH    26
#define OPERATION_BUF_SIZE  7
#define NAME_BUF_SIZE      22

struct trie_node{
    int prefix_count;
    struct trie_node *children[ALPHABET_LENGTH + 1];
};

void add(trie_node *node, trie_node *end, string name){
    int ascii=0;
    for (char c : name){
        ascii = c - 'a';
        if(!node->children[ascii]){
            node->children[ascii] = new trie_node{0, {nullptr}};
        }
        node = node->children[ascii];
        node->prefix_count += 1;
    }
    if (!node->children[ALPHABET_LENGTH]) {
        node->children[ALPHABET_LENGTH] = end;
    }
}

int find(trie_node *node, string partial){
    int ascii=0;
    for(char c: partial){
        ascii = c - 'a';
        if(!node -> children[ascii]){
            return 0;
        }
        node = node->children[ascii];
    }
    return node->prefix_count;
}

string search(trie_node *node, string word){
    int idx=0, ascii=0, strLen=word.length();
    for(idx=0; idx<strLen; idx++){
        ascii = word[idx] - 'a';
        if (!node -> children[ascii]){
            return "No";
        }
        node = node -> children[ascii];
    }
    if (!node->children[ALPHABET_LENGTH]){
        return "No";
    }
    return "Yes";
}

void lowercase(char *command, char *value){
    int idx=0, ascii=0;
    
    while(command[idx]){
        ascii = command[idx];
        if (ascii >= 65 && ascii <= 90){
            command[idx] = ascii+32;
        }
        ++idx;
    }

    idx=0;
    while(value[idx]){
        ascii = value[idx];
        if (ascii >= 65 && ascii <= 90){
            value[idx] = ascii+32;
        }
        ++idx;
    }
}

int main(int argc,  char **argv){

    int idx=1, count=0;
    string str;
    trie_node node{0, {nullptr}}, end{0, {nullptr}};

    
    while (idx<argc){

        lowercase(argv[idx], argv[idx+1]);

        if (strcmp(argv[idx], "add") == 0){
            node.prefix_count += 1; // Increment Root Node Counter (Total)
            add(&node, &end, argv[idx+1]);
        }
        else if (strcmp(argv[idx], "find") == 0){
            count += find(&node, argv[idx+1]);
        }
        else if (strcmp(argv[idx], "search") == 0){
            str = search(&node, argv[idx+1]);
        }
        idx+=2;
    }
    cout << "[" << count << ", " << str << "]" << "\n";
}