#ifndef _verify_solution_hpp_
#define _verify_solution_hpp_

//@HEADER
// ************************************************************************
//
// MiniFE: Simple Finite Element Assembly and Solve
// Copyright (2006-2013) Sandia Corporation
//
// Under terms of Contract DE-AC04-94AL85000, there is a non-exclusive
// license for use of this work by or on behalf of the U.S. Government.
//
// This library is free software; you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as
// published by the Free Software Foundation; either version 2.1 of the
// License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
// USA
//
// ************************************************************************
//@HEADER

#include <sstream>
#include <stdexcept>
#include <map>
#include <algorithm>

#include "../../../app/miniFE_openmp-2.0-rc3/basic/box_utils.hpp"
#include "../../../app/miniFE_openmp-2.0-rc3/fem/analytic_soln.hpp"
#include "../../../app/miniFE_openmp-2.0-rc3/src/simple_mesh_description.hpp"
#include "../../../app/miniFE_openmp-2.0-rc3/utils/utils.hpp"

#ifdef HAVE_MPI
#include <mpi.h>
#endif

namespace miniFE {

template<typename Scalar>
struct err_info {
  Scalar err;
  Scalar computed;
  Scalar analytic;
  Scalar coords[3];
};

template<typename VectorType>
int
verify_solution(const simple_mesh_description<typename VectorType::GlobalOrdinalType>& mesh,
                const VectorType& x, double tolerance, bool verify_whole_domain = false)
{
  typedef typename VectorType::GlobalOrdinalType GlobalOrdinal;
  typedef typename VectorType::ScalarType Scalar;

  int global_nodes_x = mesh.global_box[0][1]+1;
  int global_nodes_y = mesh.global_box[1][1]+1;
  int global_nodes_z = mesh.global_box[2][1]+1;
  Box box;
  copy_box(mesh.local_box, box);

  //num-owned-nodes in each dimension is num-elems+1
  //only if num-elems > 0 in that dimension *and*
  //we are at the high end of the global range in that dimension:
  if (box[0][1] > box[0][0] && box[0][1] == mesh.global_box[0][1]) ++box[0][1];
  if (box[1][1] > box[1][0] && box[1][1] == mesh.global_box[1][1]) ++box[1][1];
  if (box[2][1] > box[2][0] && box[2][1] == mesh.global_box[2][1]) ++box[2][1];

  std::vector<GlobalOrdinal> rows;
  std::vector<Scalar> row_coords;

  int roffset = 0;
  for(int iz=box[2][0]; iz<box[2][1]; ++iz) {
   for(int iy=box[1][0]; iy<box[1][1]; ++iy) {
    for(int ix=box[0][0]; ix<box[0][1]; ++ix) {
      GlobalOrdinal row_id =
          get_id<GlobalOrdinal>(global_nodes_x, global_nodes_y, global_nodes_z,
                                ix, iy, iz);
      Scalar x, y, z;
      get_coords(row_id, global_nodes_x, global_nodes_y, global_nodes_z, x, y, z);

      bool verify_this_point = false;
      if (verify_whole_domain) verify_this_point = true;
      else if (std::abs(x - 0.5) < 0.05 && std::abs(y - 0.5) < 0.05 && std::abs(z - 0.5) < 0.05) {
        verify_this_point = true;
      }

      if (verify_this_point) {
        rows.push_back(roffset);
        row_coords.push_back(x);
        row_coords.push_back(y);
        row_coords.push_back(z);
      }

      ++roffset;
    }
   }
  }

  int return_code = 0;

  const int num_terms = 300;

  err_info<Scalar> max_error;
  max_error.err = 0.0;

  for(size_t i=0; i<rows.size(); ++i) {
    Scalar computed_soln = x.coefs[rows[i]];
    Scalar x = row_coords[i*3];
    Scalar y = row_coords[i*3+1];
    Scalar z = row_coords[i*3+2];
    Scalar analytic_soln = 0.0;
    //set exact boundary-conditions:
    if (x == 1.0) {
      //x==1 is first, we want soln to be 1 even around the edges
      //of the x==1 plane where y and/or z may be 0 or 1...
      analytic_soln = 1;
    }
    else if (x == 0.0 || y == 0.0 || z == 0.0) {
      analytic_soln = 0;
    }
    else if (y == 1.0 || z == 1.0) {
      analytic_soln = 0;
    }
    else {
      analytic_soln = soln(x, y, z, num_terms, num_terms);
    }

#ifdef MINIFE_DEBUG_VERBOSE
std::cout<<"("<<x<<","<<y<<","<<z<<") row "<<rows[i]<<": computed: "<<computed_soln<<",  analytic: "<<analytic_soln<<std::endl;
#endif
    Scalar err = std::abs(analytic_soln - computed_soln);
    if (err > max_error.err) {
      max_error.err = err;
      max_error.computed = computed_soln;
      max_error.analytic = analytic_soln;
      max_error.coords[0] = x;
      max_error.coords[1] = y;
      max_error.coords[2] = z;
    }
  }

  Scalar local_max_err = max_error.err;
  Scalar global_max_err = 0;
#ifdef HAVE_MPI
  MPI_Allreduce(&local_max_err, &global_max_err, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);
#else
  global_max_err = local_max_err;
#endif

  if (local_max_err == global_max_err) {
    if (max_error.err > tolerance) {
      std::cout << "max absolute error is "<<max_error.err<<":"<<std::endl;
      std::cout << "   at position ("<<max_error.coords[0]<<","<<max_error.coords[1]<<","<<max_error.coords[2]<<"), "<<std::endl;
      std::cout << "   computed solution: "<<max_error.computed<<",  analytic solution: "<<max_error.analytic<<std::endl;
    }
    else {
      std::cout << "solution matches analytic solution to within "<<tolerance<<" or better."<<std::endl;
    }
  }

  if (global_max_err > tolerance) {
    return_code = 1;
  }

  return return_code;
}

}//namespace miniFE

#endif

