#include <Eigen/Dense>

std::tuple<Eigen::ArrayX3d, Eigen::ArrayXd> non_maximum_suppression(Eigen::ArrayX3d circles,
                                                                    Eigen::ArrayXd fitting_scores);
