from natsort import natsorted
from helpers.storage_helper import StorageHelper

class Vec2Dist():
    
    @staticmethod
    def calculate_distances(compound, constituents):
        file_names_separated = {f'{word}':[] for word in [compound] + constituents}

        print(file_names_separated)

        file_names = StorageHelper.list_files('vectors')
        for file_name in file_names:
            for word in file_names_separated.keys():
                if word in file_name:
                    file_names_separated[word].append(file_name)
                    break

        for word in file_names_separated.keys():
            file_names_separated[word] = natsorted(file_names_separated[word])
            # print(f'Key: {word} \n Value: {vectors[word]}')

        vectors = {f'{word}':[StorageHelper.load_vec(file_name) for file_name in file_names_separated[word]] for word in [compound] + constituents}

        # distances  = aggregator(comp_vecs, consts_vecs)
        # StorageHelper.save_distances(distances, file_name)


    def agg_sep(compound, constituents, vectors):
        means = {}
        results = [cos(vectors[compound][i], constituents[constituent][i] for i in range len(vectors[compound]))]
        for vec in vectors[compound]:

        default/cupcake_0
        write as cupcake_sep.tsv

    # load the vectors in the parent method
    # reading from disk each time is probably slower than accessing it from memory
    def agg_mean_pre_measure(compound, constituents, file_names_separated):
        n = len(file_names_separated[compound])

        means = {f'{word}': sum()}

        vecs_comp = [StorageHelper.load_vec(file_names_separated[compound][i]) for i in range(n)]

        mean_comp = sum(file_names_separated[compound]) / n
        means_constituents = [sum(file_names_separated[constituent]) / n for constituent in constituents]
        results = [[cos(mean_comp, means_constituents[i]) for i in range(n)]]
        return results
    
    def cos(vec_0)
