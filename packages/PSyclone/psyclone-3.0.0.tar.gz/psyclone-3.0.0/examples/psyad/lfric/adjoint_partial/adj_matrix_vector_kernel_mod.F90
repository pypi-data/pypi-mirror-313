module adj_matrix_vector_kernel_mod
  use argument_mod, only : any_space_1, any_space_2, arg_type, cell_column, gh_field, gh_inc, gh_operator, gh_read, gh_real
  use constants_mod, only : i_def, r_double, r_single
  use kernel_mod, only : kernel_type
  implicit none
  interface matrix_vector_code
    module procedure :: adj_matrix_vector_code_r_single, adj_matrix_vector_code_r_double
  end interface matrix_vector_code
  type, public, extends(kernel_type) :: adj_matrix_vector_kernel_type
  type(ARG_TYPE) :: META_ARGS(3) = (/ &
    arg_type(gh_field, gh_real, gh_read, any_space_1), &
    arg_type(gh_field, gh_real, gh_inc, any_space_2), &
    arg_type(gh_operator, gh_real, gh_read, any_space_1, any_space_2)/)
  INTEGER :: OPERATES_ON = cell_column
  CONTAINS
    PROCEDURE, NOPASS :: adj_matrix_vector_code_r_single
END TYPE adj_matrix_vector_kernel_type

  private

  public :: matrix_vector_code

  contains
  subroutine adj_matrix_vector_code_r_single(cell, nlayers, lhs, x, ncell_3d, matrix, ndf1, undf1, map1, ndf2, undf2, map2)
    integer(kind=i_def), intent(in) :: cell
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ncell_3d
    integer(kind=i_def), intent(in) :: undf1
    integer(kind=i_def), intent(in) :: ndf1
    integer(kind=i_def), intent(in) :: undf2
    integer(kind=i_def), intent(in) :: ndf2
    integer(kind=i_def), dimension(ndf1), intent(in) :: map1
    integer(kind=i_def), dimension(ndf2), intent(in) :: map2
    real(kind=r_single), dimension(undf2), intent(inout) :: x
    real(kind=r_single), dimension(undf1), intent(in) :: lhs
    real(kind=r_single), dimension(ncell_3d,ndf1,ndf2), intent(in) :: matrix
    integer(kind=i_def) :: df
    integer(kind=i_def) :: df2
    integer(kind=i_def) :: k
    integer(kind=i_def) :: ik

    do df = ndf1, 1, -1
      do df2 = ndf2, 1, -1
        do k = nlayers - 1, 0, -1
          ik = cell * nlayers + k - nlayers + 1
          x(k + map2(df2)) = x(k + map2(df2)) + matrix(ik,df,df2) * lhs(map1(df) + k)
        enddo
      enddo
    enddo

  end subroutine adj_matrix_vector_code_r_single
  subroutine adj_matrix_vector_code_r_double(cell, nlayers, lhs, x, ncell_3d, matrix, ndf1, undf1, map1, ndf2, undf2, map2)
    integer(kind=i_def), intent(in) :: cell
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ncell_3d
    integer(kind=i_def), intent(in) :: undf1
    integer(kind=i_def), intent(in) :: ndf1
    integer(kind=i_def), intent(in) :: undf2
    integer(kind=i_def), intent(in) :: ndf2
    integer(kind=i_def), dimension(ndf1), intent(in) :: map1
    integer(kind=i_def), dimension(ndf2), intent(in) :: map2
    real(kind=r_double), dimension(undf2), intent(inout) :: x
    real(kind=r_double), dimension(undf1), intent(in) :: lhs
    real(kind=r_double), dimension(ncell_3d,ndf1,ndf2), intent(in) :: matrix
    integer(kind=i_def) :: df
    integer(kind=i_def) :: df2
    integer(kind=i_def) :: k
    integer(kind=i_def) :: ik

    do df = ndf1, 1, -1
      do df2 = ndf2, 1, -1
        do k = nlayers - 1, 0, -1
          ik = cell * nlayers + k - nlayers + 1
          x(k + map2(df2)) = x(k + map2(df2)) + matrix(ik,df,df2) * lhs(map1(df) + k)
        enddo
      enddo
    enddo

  end subroutine adj_matrix_vector_code_r_double

end module adj_matrix_vector_kernel_mod
