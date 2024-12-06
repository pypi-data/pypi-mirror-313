#include <thrust/transform_reduce.h>
#include <thrust/device_vector.h>
#include <thrust/sequence.h>
#include <cuComplex.h>
#include <iostream>
#include <float.h>
#include <limits>

#include <thrust/host_vector.h>
#include <thrust/random.h>

__device__ float point_to_point(cuFloatComplex p1, cuFloatComplex p2)
{
    float dx = cuCrealf(p1) - cuCrealf(p2);
    float dy = cuCimagf(p1) - cuCimagf(p2);
    return sqrtf(dx * dx + dy * dy);
}

__device__ float point_to_segment(cuFloatComplex p, cuFloatComplex seg_a, cuFloatComplex seg_b)
{
    // vactor ab
    cuFloatComplex ab = make_cuFloatComplex(cuCrealf(seg_b) - cuCrealf(seg_a), cuCimagf(seg_b) - cuCimagf(seg_a));
    // vector ap
    cuFloatComplex ap = make_cuFloatComplex(cuCrealf(p) - cuCrealf(seg_a), cuCimagf(p) - cuCimagf(seg_a));
    // projection of `p` onto `ab`
    // coeff = (abx*apx + aby*apy) / (abx*abx + aby*aby)
    // dx = ax + abx * coeff
    // dy = ay + aby * coeff
    float proj_coeff = fmaxf(0, fminf(1, (cuCrealf(ab) * cuCrealf(ap) + cuCimagf(ab) * cuCimagf(ap)) / (cuCrealf(ab) * cuCrealf(ab) + cuCimagf(ab) * cuCimagf(ab))));
    // if coeff is 1 ==> the distance between p and seg is the distance between p and b
    // if coef is 0 ==> the distance between p and seg is the distance between p and a
    // if coef is in (0, 1) the distance between p and seg is the distance between p and its projection onto ab
    cuFloatComplex closest_dist = make_cuFloatComplex(cuCrealf(seg_a) + proj_coeff * cuCrealf(ab), cuCimagf(seg_a) + proj_coeff * cuCimagf(ab));
    return point_to_point(closest_dist, p);
}

struct Point_To_Trajectory_Functor
{
    cuFloatComplex *segments;
    int len;

    Point_To_Trajectory_Functor(cuFloatComplex *s, int l) : segments(s), len(l) {}

    __device__ float operator()(cuFloatComplex p) const
    {
        float min_dist = FLT_MAX;
        for (int i = 0; i < len; ++i)
        {
            cuFloatComplex a = segments[2 * i];
            cuFloatComplex b = segments[2 * i + 1];
            float dist = point_to_segment(p, a, b);
            if (dist < min_dist)
            {
                min_dist = dist;
            }
        }
        return min_dist;
    }
};

float D_spd(thrust::device_vector<cuFloatComplex> &points, thrust::device_vector<cuFloatComplex> &segments)
{
    int len_points = points.size();
    int len_segments = segments.size() / 2;

    // Apply the Point_To_Trajectory_Functor to each point in parallel
    float total_distance = thrust::transform_reduce(
        points.begin(), points.end(),
        Point_To_Trajectory_Functor(thrust::raw_pointer_cast(segments.data()), len_segments),
        0.0f, thrust::plus<float>());

    // Calculate the mean distance
    return total_distance / len_points;
}

float compute_sspd(std::vector<cuFloatComplex> &segments1, std::vector<cuFloatComplex> &segments2)
{
    thrust::device_vector<cuFloatComplex> d_segments1(segments1);
    thrust::device_vector<cuFloatComplex> d_segments2(segments2);

    float d_spd_1_to_2 = D_spd(d_segments1, d_segments2);
    float d_spd_2_to_1 = D_spd(d_segments2, d_segments1);

    return (d_spd_1_to_2 + d_spd_2_to_1) / 2.0f;
}

int main()
{
    // Example usage
    std::vector<cuFloatComplex> segments1 = {
        make_cuFloatComplex(0.0f, 0.0f), make_cuFloatComplex(1.0f, 1.0f),
        make_cuFloatComplex(1.0f, 1.0f), make_cuFloatComplex(2.0f, 2.0f)};

    std::vector<cuFloatComplex> segments2 = {
        make_cuFloatComplex(2.0f, 0.0f), make_cuFloatComplex(3.0f, 1.0f),
        make_cuFloatComplex(3.0f, 1.0f), make_cuFloatComplex(4.0f, 2.0f)};

    float sspd = compute_sspd(segments1, segments2);
    std::cout << "SSPD: " << sspd << std::endl;

    return 0;
}
