def vote(votes_dict):
    key = input("Give your vote, the options are:\n"
                "yay, nay, idk\n> ").lower()
    if not key in votes_dict.keys():
        votes_dict['error'] += 1
    else:
        votes_dict[key] += 1


def print_key_votes(k, v):
    print(f"{k}: {'#' * v}")


def show_results(res_dict):
    for cur_k, cur_v in res_dict.items():
        print_key_votes(cur_k, cur_v)


tax_renewal = {
    "yay": 0,
    "nay": 0,
    "idk": 0,
    "error": 0
}
pooh_for_president = {
    "yay": 12,
    "nay": 0,
    "idk": 5,
    "error": 4
}

print("Should we implement the tax renewal?")
vote(tax_renewal)
show_results(tax_renewal)
print("\nVote Winnie the Pooh for president?")
vote(pooh_for_president)
show_results(pooh_for_president)
