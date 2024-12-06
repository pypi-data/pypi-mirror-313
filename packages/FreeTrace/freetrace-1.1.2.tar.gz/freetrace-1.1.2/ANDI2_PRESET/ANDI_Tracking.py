import numpy as np
import scipy
import sys
sys.path.append('../')
import concurrent.futures
from numba.typed import List
from module.ImageModule import make_image_seqs, make_whole_img
from module.TrajectoryObject import TrajectoryObj
from module.FileIO import write_trajectory, read_localization, read_parameters, write_trxyt, check_video_ext
from timeit import default_timer as timer
from scipy.optimize import linear_sum_assignment


def hungarian_algo_max(cost):
    cost = -np.array(cost)
    row_ind, col_ind = linear_sum_assignment(cost)
    val = -cost[row_ind, col_ind].sum()
    return row_ind, col_ind, val


def greedy_shortest(srcs, dests):
    srcs = np.array(srcs)
    dests = np.array(dests)
    distribution = []
    superposed_locals = dests
    superposed_len = len(superposed_locals)
    linked_src = [False] * len(srcs)
    linked_dest = [False] * superposed_len
    linkage = [[0 for _ in range(superposed_len)] for _ in range(len(srcs))]
    for i, src in enumerate(srcs):
        for dest, sup_local in enumerate(superposed_locals):
            segment_length = euclidian_displacement(np.array([src]), np.array([sup_local]))
            if segment_length is not None:
                linkage[i][dest] = segment_length[0]
    minargs = np.argsort(np.array(linkage).flatten())
    for minarg in minargs:
        src = minarg // superposed_len
        dest = minarg % superposed_len
        if linked_dest[dest] or linked_src[src]:
            continue
        else:
            linked_dest[dest] = True
            linked_src[src] = True
            distribution.append(linkage[src][dest])
    return distribution


def parallel_shortest(srcs, dests):
    distribution = []
    srcs = np.array(srcs)
    dests = np.array(dests)
    selected_indices = [[] for _ in range(2)]
    src_indices = np.arange(len(srcs))
    dest_indices = np.arange(len(dests))
    combs = np.array(np.meshgrid(src_indices, dest_indices)).T.reshape(-1, 2)
    tmp = euclidian_displacement(srcs[combs[:, 0]], dests[combs[:, 1]])
    sorted_indices = np.argsort(tmp)
    combs = combs[sorted_indices]
    for (a, b), i in zip(combs, sorted_indices):
        if a not in selected_indices[0] and b not in selected_indices[1]:
            distribution.append(tmp[i])
            selected_indices[0].append(a)
            selected_indices[1].append(b)
    return distribution


def collect_segments(localization, time_steps, method, lag):
    tmp = []
    for i, time_step in enumerate(time_steps[:-lag-1]):
        srcs = localization[time_step]
        dests = localization[time_step + lag + 1]
        dists = method(srcs=srcs, dests=dests)
        tmp.extend(dists)
    return tmp


def trajectory_to_segments(trajectory_list, blink_lag):
    segment_distrib = {lag: [] for lag in range(blink_lag + 1)}
    for traj_obj in trajectory_list:
        pos = traj_obj.get_positions()
        times = traj_obj.get_times()
        for lag in range(blink_lag + 1):
            for i in range(len(pos) - 1 - lag):
                x, y, z = pos[i]
                next_x, next_y, next_z = pos[i+1+lag]
                t = times[i]
                next_t = times[i+1+lag]
                if (int(next_t - t) - 1) in segment_distrib:
                    segment_distrib[int(next_t - t) - 1].append(
                        [np.sqrt((next_x - x)**2 + (next_y - y)**2 + (next_z - z)**2)]
                    )
    for lag in segment_distrib:
        segment_distrib[lag] = np.array(segment_distrib[lag])
    return segment_distrib


def count_localizations(localization):
    nb = 0
    xyz_min = np.array([1e5, 1e5, 1e5])
    xyz_max = np.array([-1e5, -1e5, -1e5])
    time_steps = np.sort(list(localization.keys()))
    for t in time_steps:
        if localization[t].shape[1] > 0:
            x_ = np.array(localization[t])[:, 0]
            y_ = np.array(localization[t])[:, 1]
            z_ = np.array(localization[t])[:, 2]
            xyz_min = [min(xyz_min[0], np.min(x_)), min(xyz_min[1], np.min(y_)), min(xyz_min[2], np.min(z_))]
            xyz_max = [max(xyz_max[0], np.max(x_)), max(xyz_max[1], np.max(y_)), max(xyz_max[2], np.max(z_))]
            nb += len(localization[t])
    nb_per_time = nb / len(time_steps)
    return np.array(time_steps), nb_per_time, np.array(xyz_min), np.array(xyz_max)


def distribution_segments(localization: dict, time_steps: np.ndarray, lag=2,
                          parallel=False):
    seg_distribution = {}
    executors = {}
    for i in range(lag + 1):
        seg_distribution[i] = []
    if parallel:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for lag_val in seg_distribution:
                future = executor.submit(collect_segments, localization, time_steps,
                                         parallel_shortest, lag_val)
                executors[lag_val] = future
            for lag_val in seg_distribution:
                seg_distribution[lag_val] = executors[lag_val].result()
    else:
        for i, time_step in enumerate(time_steps[:-lag-1:1]):
            dests = [[] for _ in range(lag + 1)]
            srcs = localization[time_step]
            for j in range(i+1, i+lag+2):
                dest = localization[time_steps[j]]
                dests[j - i - 1].extend(dest)
            for l, dest in enumerate(dests):
                dist = greedy_shortest(srcs=srcs, dests=dest)
                seg_distribution[l].extend(dist)
    return seg_distribution


def euclidian_displacement(pos1, pos2):
    if len(pos1) == 0 or len(pos2) == 0:
        return None
    if pos1.ndim == 2 and pos1.shape[1] == 0 or pos2.ndim == 2 and pos2.shape[1] == 0:
        return None
    if pos1.ndim == 1 and len(pos1) < 3:
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    elif pos1.ndim == 1 and len(pos1) == 3:
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)
    elif pos1.ndim == 2 and pos1.shape[1] == 3:
        return np.sqrt((pos1[:, 0] - pos2[:, 0])**2 + (pos1[:, 1] - pos2[:, 1])**2 + (pos1[:, 2] - pos2[:, 2])**2)
    elif pos1.ndim == 2 and pos1.shape[1] < 3:
        return np.sqrt((pos1[:, 0] - pos2[:, 0]) ** 2 + (pos1[:, 1] - pos2[:, 1]) ** 2)


def approx_cdf(distribution, conf, bin_size, approx, n_iter, burn):
    bin_size *= 2
    length_max_val = np.max(distribution)
    bins = np.arange(0, length_max_val + bin_size, bin_size)
    hist = np.histogram(distribution, bins=bins)
    hist_dist = scipy.stats.rv_histogram(hist)
    pdf = hist[0] / np.sum(hist[0])
    bin_edges = hist[1]
    pdf = np.where(pdf > 0.0005, pdf, 0)
    pdf = pdf / np.sum(pdf)
    if approx == 'metropolis_hastings':
        distribution = metropolis_hastings(pdf, n_iter=n_iter, burn=burn) * bin_size
        reduced_bins = np.arange(0, length_max_val + bin_size, bin_size)
        hist = np.histogram(distribution, bins=reduced_bins)
        hist_dist = scipy.stats.rv_histogram(hist)
        pdf = hist[0] / np.sum(hist[0])
        bin_edges = hist[1]
    X = np.linspace(0, length_max_val + bin_size, 1000)
    for threshold, ax_val in zip(X, hist_dist.cdf(X)):
        if ax_val > conf:
            return np.quantile(distribution, 0.995), pdf, bin_edges, hist_dist.cdf, distribution


def mcmc_parallel(real_distribution, conf, bin_size, amp_factor, approx='metropolis_hastings',
                  n_iter=1e6, burn=0, parallel=True, thresholds=None):
    for lag_key in real_distribution:
        real_distribution[lag_key] = np.array(real_distribution[lag_key])
    approx_distribution = {}
    n_iter = int(n_iter)
    if parallel:
        executors = {}
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for lag in real_distribution.keys():
                future = executor.submit(approx_cdf, real_distribution[lag], conf, bin_size, approx, n_iter, burn)
                executors[lag] = future
            for index, lag in enumerate(executors):
                seg_len_obv, pdf_obv, bins_obv, cdf_obv, distrib = executors[lag].result()
                if thresholds is not None:
                    approx_distribution[lag] = [thresholds[index], pdf_obv, bins_obv, cdf_obv, distrib]
                else:
                    approx_distribution[lag] = [seg_len_obv * amp_factor, pdf_obv, bins_obv, cdf_obv, distrib]
    else:
        for index, lag in enumerate(real_distribution.keys()):
            seg_len_obv, pdf_obv, bins_obv, cdf_obv, distrib = (
                approx_cdf(distribution=real_distribution[lag],
                           conf=conf, bin_size=bin_size, approx=approx, n_iter=n_iter, burn=burn))
            if thresholds is not None:
                approx_distribution[lag] = [thresholds[index], pdf_obv, bins_obv, cdf_obv, distrib]
            else:
                approx_distribution[lag] = [seg_len_obv * amp_factor, pdf_obv, bins_obv, cdf_obv, distrib]

    bin_max = -1
    for lag in real_distribution.keys():
        bin_max = max(bin_max, len(approx_distribution[lag][1]))
    for lag in real_distribution.keys():
        for index in [1, 2]:
            tmp = np.zeros(bin_max)
            if index == 1:
                tmp[:len(approx_distribution[lag][index]) - index] = approx_distribution[lag][index][:-1 - index + 1]
            else:
                tmp[:len(approx_distribution[lag][index]) - index + 1] = approx_distribution[lag][index][:-1 - index + 2]
            approx_distribution[lag][index] = tmp
    return approx_distribution


def metropolis_hastings(pdf, n_iter, burn=0.25):
    i = 0
    u = np.random.uniform(0, 1, size=n_iter)
    current_x = np.argmax(pdf)
    samples = []
    acceptance_ratio = np.array([0, 0])
    while True:
        next_x = int(np.round(np.random.normal(current_x, 1)))
        next_x = max(0, min(next_x, len(pdf) - 1))
        proposal1 = 1  
        proposal2 = 1  
        target1 = pdf[next_x]
        target2 = pdf[current_x]
        accept_proba = min(1, (target1 * proposal1) / (target2 * proposal2))
        if u[i] <= accept_proba:
            samples.append(next_x)
            current_x = next_x
            acceptance_ratio[1] += 1
        else:
            acceptance_ratio[0] += 1
        i += 1
        if i == n_iter:
            break
    return np.array(samples)[int(len(samples)*burn):]


def displacement_probability(limits, thresholds, pdfs, bins, cut=True, sorted=True):
    pdf_indices = []
    bin_size = bins[0][1] - bins[0][0]
    pdf_length = len(pdfs[0])
    alphas = np.ceil((np.sign((thresholds / limits) - 1) + 1)/2.) + 1e-8
    trav_list = ((limits / alphas) // bin_size).astype(np.uint64)
    if cut:
        for n, index in enumerate(trav_list):
            if limits[n] < thresholds[n]:
                if index < pdf_length:
                    if pdfs[n][index] > 0.:
                        pdf_indices.append([n, pdfs[n][index]])
                    else:
                        pdf_indices.append([n, 1e-8])
                else:
                    pdf_indices.append([n, np.min(pdfs[n])])
    else:
        for n, index in enumerate(trav_list):
            if index < pdf_length:
                pdf_indices.append([n, pdfs[n][index]])
            else:
                pdf_indices.append([n, np.min(pdfs[n])])
    if len(pdf_indices) == 0:
        return None, None
    pdf_indices = np.array(pdf_indices)
    if sorted:
        sorted_args = np.argsort(pdf_indices[:, 1])[::-1]
        return pdf_indices[:, 0].astype(np.uint32)[sorted_args], np.log(pdf_indices[:, 1][sorted_args])
    else:
        return pdf_indices[:, 0].astype(np.uint32), np.log(pdf_indices[:, 1])


def unpack_distribution(distrib, paused_times):
    thresholds = []
    pdfs = []
    bins = []
    for paused_time in paused_times:
        thresholds.append(distrib[paused_time][0])
        pdfs.append(distrib[paused_time][1])
        bins.append(distrib[paused_time][2])
    return thresholds, pdfs, bins


def pair_permutation(pair1, pair2, localization, local_info):
    permutated_pair = []
    pos1s = []
    pos2s = []
    pair_infos1 = []
    pair_infos2 = []
    for t, i in pair1:
        for next_t, next_i in pair2:
            permutated_pair.append([t, i, next_t, next_i])
            pos1s.append([localization[t][i][0], localization[t][i][1], localization[t][i][2]])
            pos2s.append([localization[next_t][next_i][0], localization[next_t][next_i][1], localization[next_t][next_i][2]])
            pair_infos1.append(local_info[t][i])
            pair_infos2.append(local_info[next_t][next_i])
    pos1s = np.array(pos1s)
    pos2s = np.array(pos2s)
    segLengths = euclidian_displacement(pos1s, pos2s)
    return permutated_pair, segLengths, (pos1s, pos2s), (pair_infos1, pair_infos2)


def create_2d_window(images, localizations, time_steps, pixel_size=1., window_size=(7, 7)):
    height, width = images.shape[1:]
    included_postions = np.array([0, 1])
    x_decal = int(window_size[0] / 2)
    y_decal = int(window_size[1] / 2)
    for i, time_step in enumerate(time_steps):
        image = np.zeros((height + 2*window_size[1], width + 2*window_size[0])) + 1e-10
        image[window_size[1]:window_size[1]+height, window_size[0]:window_size[0]+width] += images[i]
        positions = (np.array(localizations[time_step])[:, included_postions] * (1/pixel_size)).astype(int) + np.array(window_size)
        for locals, pos in zip(localizations[time_step], positions):
            crop = image[pos[1] - y_decal: pos[1] + y_decal + 1, pos[0] - x_decal: pos[0] + x_decal + 1].copy()
            locals.append(crop)
    return localizations


def normalization(pairs, probas):
    proba_dict = {}
    proba_dict2 = {}

    for pair in pairs:
        src_pair = tuple(pair[:2])
        proba_dict[src_pair] = []

    for pair, ent in zip(pairs, probas):
        src_pair = tuple(pair[:2])
        dest_pair = tuple(pair[2:])
        proba_dict[src_pair].append([ent, dest_pair])
    for src_pair in proba_dict:
        proba_dict[src_pair] = np.array(proba_dict[src_pair])
    for src_pair in proba_dict:
        proba_dict[src_pair][:, 0] /= np.sum(proba_dict[src_pair][:, 0])
    for pair, ent in zip(pairs, probas):
        src_pair = tuple(pair[:2])
        for entropy, dest_pair in proba_dict[src_pair]:
            proba_dict2[(src_pair, dest_pair)] = entropy
    return proba_dict2


def pair_normalization(pairs, probas):
    proba_dict = {}
    proba_dict2 = {}

    for pair in pairs:
        src_pair = tuple(pair[:2])
        proba_dict[src_pair] = []

    for pair, ent in zip(pairs, probas):
        src_pair = tuple(pair[:2])
        dest_pair = tuple(pair[2:])
        proba_dict[src_pair].append([ent, dest_pair])
    for src_pair in proba_dict:
        proba_dict[src_pair] = np.array(proba_dict[src_pair])
    for src_pair in proba_dict:
        proba_dict[src_pair][:, 0] /= np.sum(proba_dict[src_pair][:, 0])
    for pair, ent in zip(pairs, probas):
        src_pair = tuple(pair[:2])
        for entropy, dest_pair in proba_dict[src_pair]:
            proba_dict2[(src_pair, dest_pair)] = entropy

    normalized_probas = []
    for pair in pairs:
        src_pair = tuple(pair[:2])
        dest_pair = tuple(pair[2:])
        normalized_probas.append(proba_dict2[(src_pair, dest_pair)])
    return np.array(normalized_probas)


def img_kl_divergence(linkage_pairs, linkage_log_probas, linkage_imgs):
    entropies = np.array(calcul_entropy(linkage_imgs[:, 0], linkage_imgs[:, 1]))
    entropies = 1 / entropies
    normalized_probas = pair_normalization(linkage_pairs, entropies)
    return linkage_log_probas + np.log(normalized_probas)


def kl_divergence(proba, ref_proba):
    proba = np.array(proba)
    ref_proba = np.array(ref_proba)
    proba = proba / np.sum(proba)
    ref_proba = ref_proba / np.sum(ref_proba)
    return np.sum(proba * np.log(proba/ref_proba))


def calcul_entropy(bases, compares):
    entropies = []
    for base, compare in zip(bases, compares):
        base_sum = np.sum(base)
        compare_sum = np.sum(compare)
        elem1 = base / base_sum
        elem2 = compare / compare_sum
        entropy = np.sum(elem2 * np.log(elem2/elem1))
        entropies.append(entropy)
    return entropies


def proba_from_angle(p, radian):
    if radian > np.pi/2:
        radian = np.pi - radian
    piv = (np.pi/2 - radian) / (np.pi/2)
    proba = p[0] + (p[-1] - p[0]) * piv
    return proba


def proba_direction(paired_probas, paired_infos, paired_positions):
    new_proba_pairs = paired_probas.copy()
    for i, (pair, positions) in enumerate(zip(paired_infos, paired_positions)):
        info1 = pair[0]  # xvar, yvar, rho, amp
        info2 = pair[1]
        if info1[2] < -1 or info1[2] > 1:
            print("RHO has err(regression err)")
            continue
        cur_pos = positions[0][:2]  # 2D data (x,y only)
        next_pos = positions[1][:2]  # 2D data (x,y only)
        cov1 = np.array([[info1[0], -info1[2] * np.sqrt(info1[0]) * np.sqrt(info1[1])],
                         [-info1[2] * np.sqrt(info1[0]) * np.sqrt(info1[1]), info1[1]]])
        cov2 = np.array([[info2[0], -info2[2] * np.sqrt(info2[0]) * np.sqrt(info2[1])],
                         [-info2[2] * np.sqrt(info2[0]) * np.sqrt(info2[1]), info2[1]]])

        try:
            eig_vals_1, eig_vecs_1 = np.linalg.eig(cov1)
            eig_vals_2, eig_vecs_2 = np.linalg.eig(cov2)
        except Exception as e:
            print(e)
            print('cov1', cov1)
            print('cov2', cov2)
            print(info1)
            print(info2)
            sys.exit(f'Rho has err during localization')

        eig_vals = np.array([eig_vals_1, eig_vals_2])
        eig_vecs = np.array([eig_vecs_1, eig_vecs_2])
        major_args = np.array([np.argmax(eig_vals[0]), np.argmax(eig_vals[1])])
        major_axis_vector = eig_vecs[0][major_args[0]]

        stds = eig_vals[1] / np.min(eig_vals[1])
        foci_lengh = np.sqrt(abs(stds[0]**2 - stds[1]**2))
        possible_next_pos = np.array([next_pos + eig_vecs[1][major_args[1]] * foci_lengh,
                                      next_pos - eig_vecs[1][major_args[1]] * foci_lengh])
        euclid0 = euclidian_displacement(possible_next_pos[0], cur_pos)
        euclid1 = euclidian_displacement(possible_next_pos[1], cur_pos)
        if euclid0 <= 0 or euclid1 <= 0:
            new_proba_pairs[i] += np.log(0.5)
            continue
        possible_next_vecs = np.array([(possible_next_pos[0] - cur_pos) / euclidian_displacement(possible_next_pos[0], cur_pos),
                                       (possible_next_pos[1] - cur_pos) / euclidian_displacement(possible_next_pos[1], cur_pos)])
        angles = np.array([np.arccos(possible_next_vecs[0] @ major_axis_vector.T),
                           np.arccos(possible_next_vecs[1] @ major_axis_vector.T)])
        proba_range = np.array([eig_vals[0][1-major_args[0]] / np.sum(eig_vals[0]), eig_vals[0][major_args[0]] / np.sum(eig_vals[0])])
        ps = []
        for angle in angles:
            ps.append(proba_from_angle(proba_range, angle))
        p = np.max(ps)
        new_proba_pairs[i] += np.log(p)
    return new_proba_pairs


def simple_connect(localization: dict, localization_infos: dict,
                   time_steps: np.ndarray, distrib: dict, blink_lag=1, on=None, andi2_indices=None):
    if on is None:
        on = [1, 2, 3, 4]
    trajectory_dict = {}
    end_trajectories = []
    srcs_pairs = []
    trajectory_index = 0

    if andi2_indices is None:
        for i, pos in enumerate(localization[time_steps[0]]):
            if len(localization[time_steps[0]][0]) != 0:
                trajectory_dict[(1, i)] = TrajectoryObj(index=trajectory_index, localizations=localization, max_pause=blink_lag)
                trajectory_dict[(1, i)].add_trajectory_tuple(time_steps[0], i)
                trajectory_index += 1
    else:
        random_indices = set(np.arange(0, 300))
        random_indices = random_indices.difference(andi2_indices)
        for i, (pos, andi_index) in enumerate(zip(localization[time_steps[0]], andi2_indices)):
            if len(localization[time_steps[0]][0]) != 0:
                if andi_index != -1:
                    trajectory_dict[(1, i)] = TrajectoryObj(index=andi_index, localizations=localization, max_pause=blink_lag)
                    trajectory_dict[(1, i)].add_trajectory_tuple(time_steps[0], i)
                else:
                    trajectory_dict[(1, i)] = TrajectoryObj(index=random_indices.pop(), localizations=localization, max_pause=blink_lag)
                    trajectory_dict[(1, i)].add_trajectory_tuple(time_steps[0], i)
        trajectory_index = 300

    for src_i in range(len(localization[time_steps[0]])):
        if len(localization[time_steps[0]][0]) != 0:
            srcs_pairs.append([time_steps[0], src_i])

    for i in range(len(time_steps) - 1):
        next_time = time_steps[i+1]
        srcs_linked = []
        dests_linked = []
        dests_pairs = []
        linkage_pairs = []
        linkage_indices = None

        if len(localization[next_time][0]) != 0 and len(localization[time_steps[i]][0]) != 0:
            for dest_i in range(localization[next_time].shape[0]):
                dests_pairs.append([next_time, dest_i])
            pairs, seg_lengths, pair_positions, pair_infos = (
                pair_permutation(np.array(srcs_pairs), np.array(dests_pairs), localization, localization_infos))
            pairs = np.array(pairs)
            pair_positions = np.stack(pair_positions, axis=1)
            pair_infos = np.stack(pair_infos, axis=1)
            if len(pairs) > 0:
                paused_times = np.array([trajectory_dict[tuple(src_key)].get_paused_time() for src_key in pairs[:, :2]])
                track_lengths = np.array([len(trajectory_dict[tuple(src_key)].get_times()) for src_key in pairs[:, :2]])
                thresholds, pdfs, bins = unpack_distribution(distrib, paused_times)
                seg_lengths = np.array(seg_lengths)
                thresholds = np.array(thresholds)
                linkage_indices, linkage_log_probas = (
                    displacement_probability(seg_lengths, thresholds,
                                             List(pdfs), List(bins), sorted=False))

        if linkage_indices is not None:
            linkage_pairs = pairs[linkage_indices]
            track_lengths = track_lengths[linkage_indices]
            linkage_log_probas = linkage_log_probas + track_lengths * 1e-8
            linkage_positions = pair_positions[linkage_indices]
            linkage_infos = pair_infos[linkage_indices]
            potential_trajectories = [trajectory_dict[tuple(src_key)] for src_key in linkage_pairs[:, :2]]
            if 2 in on:
                linkage_log_probas = img_kl_divergence(linkage_pairs, linkage_log_probas)
            if 3 in on:
                linkage_log_probas = proba_direction(linkage_log_probas, linkage_infos, linkage_positions)
            if 4 in on:
                linkage_log_probas = (
                    directed_motion_likelihood(potential_trajectories, linkage_log_probas, linkage_infos, linkage_positions))
                linkage_log_probas += low_priority_to_newborns(potential_trajectories)

            linkage_pairs = make_graph(linkage_pairs, linkage_log_probas)
        link_pairs = []
        for pair in linkage_pairs:
            t, src_i = pair[0]
            next_t, dest_i = pair[1]
            if (t, src_i) not in srcs_linked and (next_t, dest_i) not in dests_linked:
                link_pairs.append([[t, src_i], [next_t, dest_i]])
                srcs_linked.append((t, src_i))
                dests_linked.append((next_t, dest_i))
        for link_pair in link_pairs:
            dests_pairs.remove(link_pair[1])
        link_pairs = np.array(link_pairs)

        if len(link_pairs) > 0:
            link_srcs = link_pairs[:, 0]
        else:
            link_srcs = []
        tmp = []
        for link_src in link_srcs:
            tmp.append(tuple(link_src))
        link_srcs = tmp
        suspended_trajectories = {}

        for src_key in list(trajectory_dict.keys()):
            traj = trajectory_dict[src_key]
            if traj.get_trajectory_tuples()[-1] not in link_srcs:
                traj.wait()
            else:
                for link_pair in link_pairs:
                    if (traj.get_trajectory_tuples()[-1][0] == link_pair[0][0] and
                            traj.get_trajectory_tuples()[-1][1] == link_pair[0][1]):
                        traj.add_trajectory_tuple(link_pair[1][0], link_pair[1][1])
                        trajectory_dict[(link_pair[1][0], link_pair[1][1])] = traj
                        del trajectory_dict[src_key]
                        break
            if traj.trajectory_status():
                suspended_trajectories[src_key] = traj
                continue

        for src_key in suspended_trajectories:
            del trajectory_dict[src_key]
            end_trajectories.append(suspended_trajectories[src_key])
        for dests_pair in dests_pairs:
            trajectory_dict[(dests_pair[0], dests_pair[1])] = (
                TrajectoryObj(index=trajectory_index, localizations=localization, max_pause=blink_lag))
            trajectory_dict[(dests_pair[0], dests_pair[1])].add_trajectory_tuple(dests_pair[0], dests_pair[1])
            trajectory_index += 1
        srcs_pairs = []
        for src_key in trajectory_dict:
            traj = trajectory_dict[src_key]
            cur_t, cur_i = traj.get_trajectory_tuples()[-1]
            srcs_pairs.append([cur_t, cur_i])

    for src_key in trajectory_dict:
        trajectory_dict[src_key].close()
        end_trajectories.append(trajectory_dict[src_key])
    return end_trajectories


def optimal_next_position(localizations, optimal_trajectory, reduced_trajectory, paused_time, distrib):
    first_position = optimal_trajectory[-1]
    segment_lengths = []
    for next_position in reduced_trajectory:
        segment_lengths.append(euclidian_displacement(localizations[first_position[0]][first_position[1]],
                                                      localizations[next_position[0]][next_position[1]]))
    next_index = displacement_probability(segment_lengths, [paused_time for _ in range(len(segment_lengths))],
                            distrib, cut=False)[0][0]
    next_position = reduced_trajectory[next_index]
    reduced_trajectory.remove(next_position)
    optimal_trajectory.append(next_position)
    return optimal_trajectory, reduced_trajectory


def make_graph(pairs, probas):
    links = []
    pairs = np.array(pairs)
    probas = np.array(probas)
    assert pairs.shape[0] == probas.shape[0]
    args = np.lexsort((pairs[:, 1], pairs[:, 0]))  # sort by frame and then by molecule number
    pairs = pairs[args]
    probas = probas[args]

    sub_graphs = [[(pairs[0][0], pairs[0][1]), (pairs[0][2], pairs[0][3])]]
    pair_probas = {}
    for pair, proba in zip(pairs, probas):
        pair_probas[pair[0], pair[1], pair[2], pair[3]] = proba

    for pair in pairs[1:]:
        flag = 0
        prev_pair_tuple = (pair[0], pair[1])
        next_pair_tuple = (pair[2], pair[3])
        for sub_graph in sub_graphs:
            if prev_pair_tuple in sub_graph or next_pair_tuple in sub_graph:
                sub_graph.extend([prev_pair_tuple, next_pair_tuple])
                flag = 1
                break
        if flag == 0:
            sub_graphs.append([prev_pair_tuple, next_pair_tuple])

    while True:
        original_sub_graphs = sub_graphs.copy()
        for i in range(len(sub_graphs)):
            sub_graphs = merge_graphs(sub_graphs[i], sub_graphs, i)
            if sub_graphs != original_sub_graphs:
                break
        if sub_graphs == original_sub_graphs:
            break

    for sub_graph in sub_graphs:
        linkages, val = graph_matrix(sub_graph, pair_probas)
        for linkage in linkages:
            links.append(linkage)
    return links


def merge_graphs(graph, sub_graphs, index):
    graph_prevs = list(set([point for point in graph[::2]]))
    graph_nexts = list(set([point for point in graph[1::2]]))
    for i in range(len(sub_graphs)):
        if i == index:
            continue
        else:
            sub_graph = sub_graphs[i]
            sub_graph_prevs = list(set([point for point in sub_graph[::2]]))
            sub_graph_nexts = list(set([point for point in sub_graph[1::2]]))

            for prev, next in zip(graph_prevs, graph_nexts):
                if prev in sub_graph_prevs or next in sub_graph_nexts:
                    sub_graphs[i].extend(graph)
                    return sub_graphs[:index] + sub_graphs[index+1:]
    return sub_graphs


def graph_matrix(graph, pair_proba):
    opt_matchs = []
    default_val = -1e5
    row_list = list(set([prev_point for prev_point in graph[::2]]))
    col_list = list(set([prev_point for prev_point in graph[1::2]]))

    graph_mat = np.zeros((len(row_list), len(col_list))) + default_val
    for r, row in enumerate(row_list):
        for c, col in enumerate(col_list):
            if (row[0], row[1], col[0], col[1]) in pair_proba:
                graph_mat[r, c] = pair_proba[(row[0], row[1], col[0], col[1])]
    rows, cols, val = hungarian_algo_max(graph_mat)
    for row, col in zip(rows, cols):
        if graph_mat[row, col] > default_val + 1:
            opt_matchs.append((row_list[row], col_list[col]))
    return opt_matchs, val


def bi_variate_normal_pdf(xy, cov, mu, normalization=True):
    a = np.ones((cov.shape[0], xy.shape[0], xy.shape[1])) * (xy - mu)
    if normalization:
        return (np.exp((-1./2) * np.sum(a @ np.linalg.inv(cov) * a, axis=2))
                / (2 * np.pi * np.sqrt(np.linalg.det(cov).reshape(-1, 1))))
    else:
        return (np.exp((-1./2) * np.sum(a @ np.linalg.inv(cov) * a, axis=2)))


def dm_likelihood(sigma, traget_position, center_pos):
    cov_mat = np.array([[[sigma, 0], [0, sigma]]])
    likelihood = bi_variate_normal_pdf(
        np.array([traget_position]), cov_mat, center_pos, normalization=False).flatten()[0]
    return likelihood


def directed_motion_likelihood(trajectories, linkage_log_probas, linkage_infos, linkage_positions):
    t = 3
    k = 5
    directed_log_likelihood = []
    for traj, (prev_pos, target_pos) in zip(trajectories, linkage_positions):
        center_pos, vec_norm = traj.get_expected_pos(t)
        sigma = k
        l = dm_likelihood(sigma, target_pos[:2], center_pos[:2])
        directed_log_likelihood.append(np.log(l))

    for i, l in enumerate(directed_log_likelihood):
        if l < -9999.:
            directed_log_likelihood[i] = -9999.

    directed_log_likelihood = np.array(directed_log_likelihood)
    return linkage_log_probas + directed_log_likelihood


def low_priority_to_newborns(trajectories):
    myp = []
    for traj in trajectories:
        my_len = traj.get_trajectory_length()
        if my_len <= 1:
            myp.append(-3)
        else:
            myp.append(0)
    return np.array(myp)


def get_and2_indice(idx_img, loc):
    first_loc_copy = loc[1].copy()
    andi2_indices = [-1] * first_loc_copy.shape[0]
    ind_ = np.argwhere(idx_img < 255)

    registered_indice = []
    for andi_args in ind_:
        possible_lengths = []
        for x, y, z in first_loc_copy.astype(int):
            possible_lengths.append(np.sqrt((y - andi_args[0]) ** 2 + (x - andi_args[1]) ** 2))

        if idx_img[andi_args[0]][andi_args[1]] not in registered_indice:
            andi2_indices[np.argmin(possible_lengths)] = idx_img[andi_args[0]][andi_args[1]]
            first_loc_copy[np.argmin(possible_lengths)] = [9999999., 999999., 0.]
        registered_indice.append(idx_img[andi_args[0]][andi_args[1]])

    for i, index in enumerate(andi2_indices):
        index_sum = np.sum(idx_img == index)
        if index_sum <= 1:
            andi2_indices[i] = -1
    return np.array(andi2_indices)


if __name__ == '__main__':
    params = read_parameters('./andi2_config.txt')
    input_tif = params['tracking']['VIDEO']
    OUTPUT_DIR = params['tracking']['OUTPUT_DIR']
    blink_lag = params['tracking']['BLINK_LAG']
    cutoff = params['tracking']['CUTOFF']
    var_parallel = params['tracking']['VAR_PARALLEL']
    amp = params['tracking']['AMP_MAX_LEN']
    visualization = params['tracking']['TRACK_VISUALIZATION']
    pixel_microns = params['tracking']['PIXEL_MICRONS']
    frame_rate = params['tracking']['FRAME_PER_SEC']

    output_xml = f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_traces.xml'
    output_trj = f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_traces.csv'
    output_trxyt = f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_traces.trxyt'
    output_imgstack = f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_traces.tiff'
    output_img = f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_traces.png'

    final_trajectories = []
    methods = [1, 3, 4]
    confidence = 0.995
    THRESHOLDS = None

    images, idx_img = check_video_ext(params['localization']['VIDEO'], andi2=True)
    loc, loc_infos = read_localization(f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_loc.csv', images)
    andi2_indices = get_and2_indice(idx_img, loc)
    time_steps, mean_nb_per_time, xyz_min, xyz_max = count_localizations(loc)
    print(f'Mean nb of particles per frame: {mean_nb_per_time:.2f} particles/frame')

    start_time = timer()
    raw_segment_distribution = distribution_segments(loc, time_steps=time_steps, lag=blink_lag,
                                                     parallel=False)
    bin_size = np.mean(xyz_max - xyz_min) / 5000.

    for repeat in range(1):
        start_time = timer()
        segment_distribution = mcmc_parallel(raw_segment_distribution, confidence, bin_size, amp, n_iter=1e7, burn=0,
                                             approx='metropolis_hastings', parallel=var_parallel, thresholds=THRESHOLDS)
        for lag in segment_distribution.keys():
            print(f'{lag}_limit_length: {segment_distribution[lag][0]}')
        trajectory_list = simple_connect(localization=loc, localization_infos=loc_infos, time_steps=time_steps,
                                         distrib=segment_distribution, blink_lag=blink_lag, on=methods, andi2_indices=andi2_indices)
        segment_distribution = trajectory_to_segments(trajectory_list, blink_lag)

    for trajectory in trajectory_list:
        if not trajectory.delete(cutoff=cutoff):
            if andi2_indices is not None:
                if trajectory.get_index() in andi2_indices:
                    final_trajectories.append(trajectory)
            else:
                final_trajectories.append(trajectory)

    andi2_indices = andi2_indices[andi2_indices > -1]
    print(f'Total number of trajectories: {len(trajectory_list)}')
    if len(andi2_indices) != 10:
        print(f'indexing err on {input_tif}')
        exit(1)
    for trajectory in trajectory_list:
        if not trajectory.delete(cutoff=cutoff):
            final_trajectories.append(trajectory)
    np.savez(f'{OUTPUT_DIR}/{input_tif.split("/")[-1].split(".tif")[0]}_vip_indices.npz', andi2_indices=np.array(andi2_indices))

    write_trajectory(output_trj, final_trajectories)
    write_trxyt(output_trxyt, final_trajectories, pixel_microns, frame_rate)
    make_whole_img(final_trajectories, output_dir=output_img, img_stacks=images)
    if visualization:
        print(f'Visualizing trajectories...')
        make_image_seqs(final_trajectories, output_dir=output_imgstack, img_stacks=images, time_steps=time_steps, cutoff=cutoff,
                        add_index=False, local_img=None, gt_trajectory=None)
