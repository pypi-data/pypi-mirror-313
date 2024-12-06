#include <cuComplex.h>

extern "C"
{
    __device__ float point_to_point(cuFloatComplex p1, cuFloatComplex p2)
    {
        float dx = cuCrealf(p1) - cuCrealf(p2);
        float dy = cuCimagf(p1) - cuCimagf(p2);
        return sqrtf(dx * dx + dy * dy);
    }

    __device__ float point_to_segment(cuFloatComplex p, cuFloatComplex seg_a, cuFloatComplex seg_b)
    {
        cuFloatComplex ab = make_cuFloatComplex(cuCrealf(seg_b) - cuCrealf(seg_a), cuCimagf(seg_b) - cuCimagf(seg_a));
        cuFloatComplex ap = make_cuFloatComplex(cuCrealf(p) - cuCrealf(seg_a), cuCimagf(p) - cuCimagf(seg_a));
        float ab_norm_sq = cuCrealf(ab) * cuCrealf(ab) + cuCimagf(ab) * cuCimagf(ab);
        float proj_coeff = fmaxf(0.0f, fminf(1.0f, (cuCrealf(ap) * cuCrealf(ab) + cuCimagf(ap) * cuCimagf(ab)) / ab_norm_sq));
        cuFloatComplex closest_point = make_cuFloatComplex(
            cuCrealf(seg_a) + proj_coeff * cuCrealf(ab),
            cuCimagf(seg_a) + proj_coeff * cuCimagf(ab));
        return point_to_point(p, closest_point);
    }

    __global__ void sspd_self_pairwise(const cuFloatComplex *trajectories,
                                       int num_trajectories, int traj_len,
                                       float *results)
    {
        // Calculate the indices for the current thread
        int pair_idx = blockIdx.x; // Index of the trajectory pair we're processing
        int tid = threadIdx.x;     // Thread ID within the block
        int stride = blockDim.x;   // Number of threads in the block

        // Convert pair_idx to (i,j) indices for upper triangular part
        int i = 0;
        int j = 0;
        int remaining = pair_idx;

        // Find i and j from pair_idx
        for (i = 0; i < num_trajectories - 1; i++)
        {
            int row_length = num_trajectories - i - 1;
            if (remaining < row_length)
            {
                j = i + 1 + remaining;
                break;
            }
            remaining -= row_length;
        }

        // Check if this is a valid pair
        if (i < num_trajectories - 1 && j < num_trajectories)
        {
            // Get pointers to the two trajectories
            const cuFloatComplex *traj_i = trajectories + i * traj_len;
            const cuFloatComplex *traj_j = trajectories + j * traj_len;

            // Process points in strided fashion
            for (int point_idx = tid; point_idx < traj_len; point_idx += stride)
            {
                // Forward direction: point from traj_i to segments in traj_j
                cuFloatComplex p_i = traj_i[point_idx];
                float min_dist_ij = 3.402823466e+38f;

                for (int k = 0; k < traj_len - 1; ++k)
                {
                    float dist = point_to_segment(p_i, traj_j[k], traj_j[k + 1]);
                    min_dist_ij = fminf(min_dist_ij, dist);
                }

                // Reverse direction: point from traj_j to segments in traj_i
                cuFloatComplex p_j = traj_j[point_idx];
                float min_dist_ji = 3.402823466e+38f;

                for (int k = 0; k < traj_len - 1; ++k)
                {
                    float dist = point_to_segment(p_j, traj_i[k], traj_i[k + 1]);
                    min_dist_ji = fminf(min_dist_ji, dist);
                }

                // Add the minimum distances (divided by 2*traj_len for averaging)
                atomicAdd(&results[pair_idx], (min_dist_ij + min_dist_ji) / (2.0f * traj_len));
            }
        }
    }
}
