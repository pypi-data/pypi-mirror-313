module adj_poly_adv_update_kernel_mod
  use argument_mod, only : any_discontinuous_space_1, arg_type, cell_column, cross2d, func_type, gh_field, gh_read, gh_readwrite, &
&gh_real, gh_write, stencil
  use constants_mod, only : i_def, l_def, r_tran
  use fs_continuity_mod, only : w2, wtheta
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: adj_poly_adv_update_kernel_type
  type(ARG_TYPE) :: META_ARGS(3) = (/ &
    arg_type(gh_field, gh_real, gh_readwrite, wtheta), &
    arg_type(gh_field, gh_real, gh_readwrite, any_discontinuous_space_1, stencil(cross2d)), &
    arg_type(gh_field, gh_real, gh_read, w2, stencil(cross2d))/)
  INTEGER :: OPERATES_ON = cell_column
  CONTAINS
    PROCEDURE, NOPASS :: adj_poly_adv_update_code
END TYPE adj_poly_adv_update_kernel_type

  private

  public :: adj_poly_adv_update_code

  contains
  subroutine adj_poly_adv_update_code(nlayers, advective, reconstruction, smap_md_size, smap_md_max, smap_md, wind, smap_w2_size, &
&smap_w2_max, smap_w2, ndf_wt, undf_wt, map_wt, ndf_md, undf_md, map_md, ndf_w2, undf_w2, map_w2)
    integer(kind=i_def), parameter :: nfaces = 4
    integer(kind=i_def), parameter :: w = 1
    integer(kind=i_def), parameter :: s = 2
    integer(kind=i_def), parameter :: e = 3
    integer(kind=i_def), parameter :: n = 4
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf_wt
    integer(kind=i_def), intent(in) :: undf_wt
    integer(kind=i_def), dimension(ndf_wt), intent(in) :: map_wt
    integer(kind=i_def), intent(in) :: ndf_md
    integer(kind=i_def), intent(in) :: undf_md
    integer(kind=i_def), dimension(ndf_md), intent(in) :: map_md
    integer(kind=i_def), intent(in) :: ndf_w2
    integer(kind=i_def), intent(in) :: undf_w2
    integer(kind=i_def), dimension(ndf_w2), intent(in) :: map_w2
    integer(kind=i_def), intent(in) :: smap_md_max
    integer(kind=i_def), dimension(4), intent(in) :: smap_md_size
    integer(kind=i_def), dimension(ndf_md,smap_md_max,4), intent(in) :: smap_md
    integer(kind=i_def), intent(in) :: smap_w2_max
    integer(kind=i_def), dimension(4), intent(in) :: smap_w2_size
    integer(kind=i_def), dimension(ndf_w2,smap_w2_max,4), intent(in) :: smap_w2
    real(kind=r_tran), dimension(undf_wt), intent(inout) :: advective
    real(kind=r_tran), dimension(undf_md), intent(inout) :: reconstruction
    real(kind=r_tran), dimension(undf_w2), intent(in) :: wind
    integer(kind=i_def) :: k
    integer(kind=i_def) :: df
    integer(kind=i_def) :: ijp
    integer(kind=i_def) :: df1
    integer(kind=i_def) :: df2
    integer(kind=i_def), dimension(4) :: direction_dofs
    real(kind=r_tran) :: direction
    real(kind=r_tran), dimension(nfaces) :: v_dot_n
    real(kind=r_tran), dimension(4,0:nlayers) :: tracer
    real(kind=r_tran), dimension(2,0:nlayers) :: uv
    real(kind=r_tran) :: dtdx
    real(kind=r_tran) :: dtdy
    integer(kind=i_def), dimension(nfaces) :: opposite
    logical(kind=l_def), dimension(nfaces) :: missing_neighbour

    tracer = 0.0_r_tran
    dtdy = 0.0_r_tran
    dtdx = 0.0_r_tran
    v_dot_n(:) = 1.0_r_tran
    v_dot_n(1) = -1.00000000000000
    v_dot_n(4) = -1.00000000000000
    opposite(:) = -1
    missing_neighbour(:) = .false.
    do df = 1, nfaces, 1
      df1 = map_w2(df)
      if (smap_w2_size(df) > 1) then
        do df2 = 1, nfaces, 1
          if (smap_w2(df2,2,df) == df1) then
            opposite(df) = df2
          end if
        enddo
      else
        opposite(df) = df
        missing_neighbour(df) = .true.
      end if
    enddo
    k = 0
    uv(1,k) = 0.25 * wind(map_w2(1)) + 0.25 * wind(map_w2(3))
    uv(2,k) = 0.25 * wind(map_w2(2)) + 0.25 * wind(map_w2(4))
    do k = 1, nlayers - 1, 1
      uv(1,k) = 0.25 * wind(k + map_w2(1)) + 0.25 * wind(k + map_w2(3)) + 0.25 * wind(k + map_w2(1) - 1) + 0.25 * wind(k + &
&map_w2(3) - 1)
      uv(2,k) = 0.25 * wind(k + map_w2(2)) + 0.25 * wind(k + map_w2(4)) + 0.25 * wind(k + map_w2(2) - 1) + 0.25 * wind(k + &
&map_w2(4) - 1)
    enddo
    k = nlayers
    uv(1,k) = 0.25 * wind(k + map_w2(1) - 1) + 0.25 * wind(k + map_w2(3) - 1)
    uv(2,k) = 0.25 * wind(k + map_w2(2) - 1) + 0.25 * wind(k + map_w2(4) - 1)
    direction_dofs(:,2) = 1
    direction_dofs(2:,2) = 2
    do k = nlayers, 0, -1
      dtdx = dtdx + advective(map_wt(1) + k) * uv(1,k)
      dtdy = dtdy - advective(map_wt(1) + k) * uv(2,k)
      advective(map_wt(1) + k) = 0.0
      tracer(n,k) = tracer(n,k) + dtdy
      tracer(s,k) = tracer(s,k) - dtdy
      dtdy = 0.0
      tracer(e,k) = tracer(e,k) + dtdx
      tracer(w,k) = tracer(w,k) - dtdx
      dtdx = 0.0
    enddo
    do df = nfaces, 1, -1
      do k = nlayers, 0, -1
        direction = uv(direction_dofs(df),k) * v_dot_n(df)
        if (direction > 0.0_r_tran .OR. missing_neighbour(df)) then
          ijp = df * nlayers + df - nlayers + map_md(1) - 1
          reconstruction(ijp + k) = reconstruction(ijp + k) + tracer(df,k)
          tracer(df,k) = 0.0
        else
          ijp = nlayers * opposite(df) - nlayers + opposite(df) + smap_md(1,2,df) - 1
          reconstruction(ijp + k) = reconstruction(ijp + k) + tracer(df,k)
          tracer(df,k) = 0.0
        end if
      enddo
    enddo

  end subroutine adj_poly_adv_update_code

end module adj_poly_adv_update_kernel_mod
