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
        float proj_coeff = fmaxf(0, fminf(1, (cuCrealf(ab) * cuCrealf(ap) + cuCimagf(ab) * cuCimagf(ap)) / (cuCrealf(ab) * cuCrealf(ab) + cuCimagf(ab) * cuCimagf(ab))));
        cuFloatComplex closest_point = make_cuFloatComplex(cuCrealf(seg_a) + proj_coeff * cuCrealf(ab), cuCimagf(seg_a) + proj_coeff * cuCimagf(ab));
        return point_to_point(closest_point, p);
    }

    __global__ void spd_cross_product(const cuFloatComplex *target_trajectories, int num_targets,
                                      const cuFloatComplex *trajectories, int num_trajectories,
                                      int traj_len, float *results)
    {
        // Calculate the indices for the current thread
        int traj_idx = blockIdx.x;   // Index of the trajectory we're processing
        int target_idx = blockIdx.y; // Index of the target trajectory we're comparing against
        int point_idx = threadIdx.x; // Index of the point within the trajectory

        // Check if the current thread is within bounds
        if (traj_idx < num_trajectories && target_idx < num_targets && point_idx < traj_len)
        {
            // Get the current point from the trajectory we're processing
            cuFloatComplex p = trajectories[traj_idx * traj_len + point_idx];

            // Initialize the minimum distance to a very large value (similar to FLT_MAX)
            float min_dist = 3.402823466e+38f;

            // Iterate through each segment of the target trajectory
            for (int i = 0; i < traj_len - 1; ++i)
            {
                // Get the start and end points of the current segment in the target trajectory
                cuFloatComplex a = target_trajectories[target_idx * traj_len + i];
                cuFloatComplex b = target_trajectories[target_idx * traj_len + i + 1];

                // Calculate the distance from the current point to the current segment
                float dist = point_to_segment(p, a, b);

                // Update the minimum distance if we found a closer segment
                if (dist < min_dist)
                {
                    min_dist = dist;
                }
            }

            // Add the minimum distance (divided by trajectory length) to the result
            // We use atomicAdd because multiple threads might be updating the same result
            atomicAdd(&results[traj_idx * num_targets + target_idx], min_dist / traj_len);
        }
    }

    __global__ void spd_pairwise(const cuFloatComplex *target_trajectories,
                                 const cuFloatComplex *trajectories,
                                 int num_trajectories, int traj_len, float *results)
    {
        // Calculate the indices for the current thread
        int traj_idx = blockIdx.x;   // Index of the trajectory pair we're processing
        int point_idx = threadIdx.x; // Index of the point within the trajectory

        // Check if the current thread is within bounds
        if (traj_idx < num_trajectories && point_idx < traj_len)
        {
            // Get the current point from the trajectory we're processing
            cuFloatComplex p = trajectories[traj_idx * traj_len + point_idx];

            // Initialize the minimum distance to a very large value (similar to FLT_MAX)
            float min_dist = 3.402823466e+38f;

            // Iterate through each segment of the corresponding target trajectory
            for (int i = 0; i < traj_len - 1; ++i)
            {
                // Get the start and end points of the current segment in the target trajectory
                cuFloatComplex a = target_trajectories[traj_idx * traj_len + i];
                cuFloatComplex b = target_trajectories[traj_idx * traj_len + i + 1];

                // Calculate the distance from the current point to the current segment
                float dist = point_to_segment(p, a, b);

                // Update the minimum distance if we found a closer segment
                if (dist < min_dist)
                {
                    min_dist = dist;
                }
            }

            // Add the minimum distance (divided by trajectory length) to the result
            // We use atomicAdd because multiple threads might be updating the same result
            atomicAdd(&results[traj_idx], min_dist / traj_len);
        }
    }
}