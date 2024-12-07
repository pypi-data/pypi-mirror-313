module adj_poly1d_w3_reconstruction_kernel_mod
  use argument_mod, only : any_discontinuous_space_1, arg_type, cell_column, cross, func_type, gh_basis, gh_evaluator, gh_field, &
&gh_inc, gh_integer, gh_read, gh_readwrite, gh_real, gh_scalar, outward_normals_to_horizontal_faces, reference_element_data_type, &
&stencil
  use constants_mod, only : i_def, r_def
  use fs_continuity_mod, only : w2, w3
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: adj_poly1d_w3_reconstruction_kernel_type
  type(ARG_TYPE) :: META_ARGS(6) = (/ &
    arg_type(gh_field, gh_real, gh_inc, w2), &
    arg_type(gh_field, gh_real, gh_read, w2), &
    arg_type(gh_field, gh_real, gh_readwrite, w3, stencil(cross)), &
    arg_type(gh_field, gh_real, gh_read, any_discontinuous_space_1), &
    arg_type(gh_scalar, gh_integer, gh_read), &
    arg_type(gh_scalar, gh_integer, gh_read)/)
  type(FUNC_TYPE) :: META_FUNCS(1) = (/ &
    func_type(w2, gh_basis)/)
  type(REFERENCE_ELEMENT_DATA_TYPE) :: META_REFERENCE_ELEMENT(1) = (/ &
    reference_element_data_type(outward_normals_to_horizontal_faces)/)
  INTEGER :: GH_SHAPE = gh_evaluator
  INTEGER :: OPERATES_ON = cell_column
  CONTAINS
    PROCEDURE, NOPASS :: adj_poly1d_w3_reconstruction_code
END TYPE adj_poly1d_w3_reconstruction_kernel_type

  private

  public :: adj_poly1d_w3_reconstruction_code

  contains
  subroutine adj_poly1d_w3_reconstruction_code(nlayers, reconstruction, wind, tracer, stencil_size, stencil_map, coeff, order, &
&ndata, ndf_w2, undf_w2, map_w2, basis_w2, ndf_w3, undf_w3, map_w3, ndf_c, undf_c, map_c, nfaces_re_h, &
&outward_normals_to_horizontal_faces)
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf_w3
    integer(kind=i_def), intent(in) :: undf_w3
    integer(kind=i_def), dimension(ndf_w3), intent(in) :: map_w3
    integer(kind=i_def), intent(in) :: ndf_w2
    integer(kind=i_def), intent(in) :: undf_w2
    integer(kind=i_def), dimension(ndf_w2), intent(in) :: map_w2
    integer(kind=i_def), intent(in) :: ndf_c
    integer(kind=i_def), intent(in) :: undf_c
    integer(kind=i_def), dimension(ndf_c), intent(in) :: map_c
    integer(kind=i_def), intent(in) :: ndata
    integer(kind=i_def), intent(in) :: order
    integer(kind=i_def), intent(in) :: stencil_size
    integer(kind=i_def), intent(in) :: nfaces_re_h
    real(kind=r_def), dimension(undf_w2), intent(inout) :: reconstruction
    real(kind=r_def), dimension(undf_w2), intent(in) :: wind
    real(kind=r_def), dimension(undf_w3), intent(inout) :: tracer
    real(kind=r_def), dimension(undf_c), intent(in) :: coeff
    real(kind=r_def), dimension(3,ndf_w2,ndf_w2), intent(in) :: basis_w2
    integer(kind=i_def), dimension(ndf_w3,stencil_size), intent(in) :: stencil_map
    real(kind=r_def), dimension(3,nfaces_re_h), intent(in) :: outward_normals_to_horizontal_faces
    integer(kind=i_def) :: k
    integer(kind=i_def) :: df
    integer(kind=i_def) :: p
    integer(kind=i_def) :: face
    integer(kind=i_def) :: stencil
    integer(kind=i_def) :: stencil_depth
    integer(kind=i_def) :: depth
    integer(kind=i_def) :: face_mod
    integer(kind=i_def) :: ijp
    real(kind=r_def) :: direction
    real(kind=r_def) :: v_dot_n
    real(kind=r_def), dimension(nlayers) :: polynomial_tracer
    integer(kind=i_def), dimension(order + 1,nfaces_re_h) :: map1d
    integer :: i
    real(kind=r_def) :: res_dot_product
    integer :: idx

    polynomial_tracer = 0.0_r_def
    stencil_depth = order / 2
    map1d(1,:) = 1
    do face = 1, nfaces_re_h, 1
      depth = 1
      face_mod = stencil_depth * MOD(face + 1, 2)
      do stencil = 2, stencil_depth + 1, 1
        map1d(stencil + depth - 1,face) = face_mod + stencil
        map1d(stencil + depth,face) = face_mod + order + stencil
        depth = depth + 1
      enddo
    enddo
    do df = nfaces_re_h, 1, -1
      res_dot_product = 0.0
      do i = 1, 3, 1
        res_dot_product = res_dot_product + basis_w2(i,df,df) * outward_normals_to_horizontal_faces(i,df)
      enddo
      v_dot_n = res_dot_product
      do k = nlayers - 1, 0, -1
        direction = v_dot_n * wind(k + map_w2(df))
        if (direction > 0.0_r_def) then
          polynomial_tracer(k) = polynomial_tracer(k) + reconstruction(map_w2(df) + k)
          reconstruction(map_w2(df) + k) = 0.0
        end if
      enddo
      do p = order + 1, 1, -1
        ijp = df * order + df - order + p + map_c(1) - 2
        stencil = map1d(p,df)
        do k = nlayers - 1, 0, -1
          tracer(k + stencil_map(1,stencil)) = tracer(k + stencil_map(1,stencil)) + coeff(ijp) * polynomial_tracer(k)
        enddo
      enddo
      do idx = UBOUND(polynomial_tracer, dim=1), LBOUND(polynomial_tracer, dim=1), -1
        polynomial_tracer(idx) = 0.0
      enddo
    enddo

  end subroutine adj_poly1d_w3_reconstruction_code

end module adj_poly1d_w3_reconstruction_kernel_mod
