"""
pybind comp
"""
from __future__ import annotations
import netgen.libngpy._meshing
import ngsolve.bla
import ngsolve.fem
import ngsolve.la
import ngsolve.ngstd
import numpy
import pyngcore.pyngcore
import typing
from . import pml
__all__ = ['APhiHCurlAMG', 'Array_N6ngcomp13COUPLING_TYPEE_S', 'BBBND', 'BBND', 'BDDCPreconditioner', 'BDDCPreconditioner_complex', 'BDDCPreconditioner_double', 'BND', 'BilinearForm', 'BndElementId', 'BoundaryFromVolumeCF', 'COUPLING_TYPE', 'ComponentGridFunction', 'Compress', 'CompressCompound', 'ContactBoundary', 'ConvertOperator', 'DifferentialSymbol', 'Discontinuous', 'DualProxyFunction', 'ElementId', 'ElementRange', 'FESpace', 'FESpaceElement', 'FESpaceElementRange', 'FacetFESpace', 'FacetSurface', 'FlatArray_N6ngcomp13COUPLING_TYPEE_S', 'FromArchiveCF', 'FromArchiveFESpace', 'FromArchiveMesh', 'GlobalInterfaceSpace', 'GlobalSpace', 'GlobalVariables', 'GridFunction', 'GridFunctionC', 'GridFunctionCoefficientFunction', 'GridFunctionD', 'H1', 'H1LumpingFESpace', 'HCurl', 'HCurlAMG', 'HCurlCurl', 'HCurlDiv', 'HDiv', 'HDivDiv', 'HDivDivSurface', 'HDivSurface', 'Hidden', 'Integral', 'Integrate', 'IntegrationRuleSpace', 'IntegrationRuleSpaceSurface', 'Interpolate', 'InterpolateProxy', 'KSpaceCoeffs', 'L2', 'LinearForm', 'LocalPreconditioner', 'MatrixFreeOperator', 'MatrixValued', 'Mesh', 'MeshNode', 'MeshNodeRange', 'MultiGridPreconditioner', 'NGS_Object', 'Ngs_Element', 'NodalFESpace', 'NodeId', 'NodeRange', 'NormalFacetFESpace', 'NormalFacetSurface', 'NumberSpace', 'ORDER_POLICY', 'PatchwiseSolve', 'Periodic', 'PlateauFESpace', 'Preconditioner', 'ProductSpace', 'Prolongate', 'ProlongateCoefficientFunction', 'Prolongation', 'ProxyFunction', 'QuasiPeriodicC', 'QuasiPeriodicD', 'Region', 'RegisterPreconditioner', 'Reorder', 'SetHeapSize', 'SetTestoutFile', 'SumOfIntegrals', 'SurfaceL2', 'SymbolTable_D', 'SymbolTable_sp_D', 'SymbolTable_sp_N5ngfem19CoefficientFunctionE', 'SymbolTable_sp_N6ngcomp10LinearFormE', 'SymbolTable_sp_N6ngcomp12BilinearFormE', 'SymbolTable_sp_N6ngcomp12GridFunctionE', 'SymbolTable_sp_N6ngcomp14PreconditionerE', 'SymbolTable_sp_N6ngcomp7FESpaceE', 'SymbolicBFI', 'SymbolicEnergy', 'SymbolicLFI', 'SymbolicTPBFI', 'TangentialFacetFESpace', 'TangentialSurfaceL2', 'TensorProductFESpace', 'TensorProductIntegrate', 'ToArchive', 'Transfer2StdMesh', 'VOL', 'VTKOutput', 'Variation', 'VectorFacetFESpace', 'VectorFacetSurface', 'VectorH1', 'VectorL2', 'VectorNodalFESpace', 'VectorSurfaceL2', 'VectorValued', 'VorB', 'ngsglobals', 'pml']
class APhiHCurlAMG(HCurlAMG):
    """
    
     Keyword arguments can be:
    inverse: 
      Inverse type used in Preconditioner.
    test: bool = False
      Computes condition number for preconditioner, if testout file
      is set, prints eigenvalues to file.
    block: 
      use block-Jacobi/block-Gauss-Seidel
    blocktype: 
      blocktype like 'vertexpatch', 'edgepatch', ...
    """
    def __init__(self, bf: BilinearForm, **kwargs) -> None:
        ...
class Array_N6ngcomp13COUPLING_TYPEE_S(FlatArray_N6ngcomp13COUPLING_TYPEE_S):
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, n: int) -> None:
        """
        Makes array of given length
        """
    @typing.overload
    def __init__(self, vec: list[COUPLING_TYPE]) -> None:
        """
        Makes array with given list of elements
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
class BDDCPreconditioner(Preconditioner):
    """
    element-level BDDC preconditioner.
    
    TODO
    
     Keyword arguments can be:
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __init__(self, bf: BilinearForm, **kwargs) -> None:
        ...
class BDDCPreconditioner_complex(BDDCPreconditioner):
    """
    
     Keyword arguments can be:
    """
class BDDCPreconditioner_double(BDDCPreconditioner):
    """
    
     Keyword arguments can be:
    """
class BilinearForm(NGS_Object):
    """
    
    Used to store the left hand side of a PDE. integrators (ngsolve.BFI)
    to it to implement your PDE. If the left hand side is linear
    you can use BilinearForm.Assemble to assemble it after adding
    your integrators. For nonlinear usage use BilinearForm.Apply or
    BilinearForm.AssembleLinearization instead of Bilinearform.Assemble.
    
    Parameters:
    
    space : ngsolve.FESpace
      The finite element space the bilinearform is defined on. This
      can be a compound FESpace for a mixed formulation.
    
    
     Keyword arguments can be:
    condense: bool = False
      (formerly known as 'eliminate_internal')
      Set up BilinearForm for static condensation of internal
      bubbles. Static condensation has to be done by user,
      this enables only the use of the members harmonic_extension,
      harmonic_extension_trans and inner_solve. Have a look at the
      documentation for further information.
    eliminate_internal: bool = False
      deprecated for static condensation, replaced by 'condense'
    
    keep_internal: bool = True
      store harmonic extension and inner inverse matrix from static condensation
      set to False to save memory, and recompute local matrices on demand
    
    store_inner: bool = False
      store inner element matrix (of static condensation)
    
    eliminate_hidden: bool = False
      Set up BilinearForm for static condensation of hidden
      dofs. May be overruled by eliminate_internal.
    print: bool = False
      Write additional information to testout file. 
      This file must be set by ngsolve.SetTestoutFile. Use 
      ngsolve.SetNumThreads(1) for serial output
    printelmat: bool = False
      Write element matrices to testout file
    symmetric: bool = False
      BilinearForm is symmetric.
      does not imply symmetric_storage, as used to be earlier
    
    symmetric_storage: bool = False
      Store only lower triangular part of sparse matrix.
    nonassemble: bool = False
      BilinearForm will not allocate memory for assembling.
      optimization feature for (nonlinear) problems where the
      form is only applied but never assembled.
    project: bool = False
      When calling bf.Assemble, all saved coarse matrices from
      mesh refinements are updated as well using a Galerkin projection
      of the matrix on the finest grid. This is needed to use the multigrid
      preconditioner with a changing bilinearform.
    nonsym_storage: bool = False
      (deprecated) The full matrix is stored, even if the symmetric flag is set.
    diagonal: bool = False
      Stores only the diagonal of the matrix.
    hermitian: bool = False
      matrix is hermitian.
    geom_free: bool = False
      when element matrices are independent of geometry, we store them 
      only for the reference elements
    matrix_free_bdb: bool = False
      store BDB factors seperately
    nonlinear_matrix_free_bdb: bool = False
      store BDB factors seperately for nonlinear operators
    check_unused: bool = True
      If set prints warnings if not UNUSED_DOFS are not used.
    delete_zero_elements: double = unset
      remove all matrix entries smaller than this value from sparse matrix
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    @typing.overload
    def Add(self, integrator: ngsolve.fem.BFI) -> BilinearForm:
        """
                 Add integrator to bilinear form.
        
        Parameters:
        
        integrator : ngsolve.fem.BFI
          input bilinear form integrator
        """
    @typing.overload
    def Add(self, arg0: SumOfIntegrals) -> typing.Any:
        ...
    @typing.overload
    def Apply(self, x: ngsolve.la.BaseVector, y: ngsolve.la.BaseVector) -> None:
        """
        Applies a (non-)linear variational formulation to x and stores the result in y.
        
        Parameters:
        
        x : ngsolve.BaseVector
          input vector
        
        y : ngsolve.BaseVector
          output vector
        """
    @typing.overload
    def Apply(self, u: ngsolve.la.BaseVector) -> ngsolve.la.DynamicVectorExpression:
        ...
    def Assemble(self, reallocate: bool = False) -> BilinearForm:
        """
        Assemble the bilinear form.
        
        Parameters:
        
        reallocate : bool
          input reallocate
        """
    def AssembleLinearization(self, ulin: ngsolve.la.BaseVector, reallocate: bool = False) -> None:
        """
        Computes linearization of the bilinear form at given vecor.
        
        Parameters:
        
        ulin : ngsolve.la.BaseVector
          input vector
        """
    def ComputeInternal(self, u: ngsolve.la.BaseVector, f: ngsolve.la.BaseVector) -> None:
        """
        Parameters:
        
        u : ngsolve.la.BaseVector
          input vector
        
        f : ngsolve.la.BaseVector
          input right hand side
        """
    def DeleteMatrix(self) -> None:
        ...
    def DeleteSpecialElements(self) -> None:
        ...
    def Energy(self, x: ngsolve.la.BaseVector) -> float:
        """
        Computes the energy of EnergyIntegrators like SymbolicEnergy for given input vector.
        
        Parameters:
        
        x : ngsolve.la.BaseVector
          input vector
        """
    def Flux(self, gf: GridFunction) -> ngsolve.fem.CoefficientFunction:
        """
        Parameters:
        
        gf : ngsolve.comp.GridFunction
          input GridFunction
        """
    def GetMatrixLevel(self, level: int | None = None) -> BaseMatrix:
        """
        returns matrix from multigrid level, default is finest level
        """
    def SetPreconditioner(self, arg0: ...) -> None:
        ...
    def UnsetPreconditioner(self, arg0: ...) -> None:
        ...
    def __call__(self, gfu: GridFunction, gfv: GridFunction) -> float:
        ...
    @typing.overload
    def __iadd__(self, other: ngsolve.fem.BFI) -> BilinearForm:
        ...
    @typing.overload
    def __iadd__(self, arg0: SumOfIntegrals) -> BilinearForm:
        ...
    @typing.overload
    def __iadd__(self, arg0: Variation) -> BilinearForm:
        ...
    @typing.overload
    def __init__(self, space: FESpace, name: str = 'biform_from_py', **kwargs) -> None:
        ...
    @typing.overload
    def __init__(self, trialspace: FESpace, testspace: FESpace, name: str = 'biform_from_py', **kwargs) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: SumOfIntegrals, **kwargs) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def components(self) -> list:
        """
        list of components for bilinearforms on compound-space
        """
    @property
    def condense(self) -> bool:
        """
        use static condensation ?
        """
    @property
    def harmonic_extension(self) -> BaseMatrix:
        """
        harmonic_extension used for static condensaition
        """
    @property
    def harmonic_extension_trans(self) -> BaseMatrix:
        """
        harmonic_extension_trans used for static condensation
        """
    @property
    def inner_matrix(self) -> BaseMatrix:
        """
        inner_matrix of the bilinear form
        """
    @property
    def inner_solve(self) -> BaseMatrix:
        """
        inner_solve used for static condensation
        """
    @property
    def integrators(self) -> tuple:
        """
        integrators of the bilinear form
        """
    @property
    def loform(self) -> BilinearForm:
        ...
    @property
    def mat(self) -> BaseMatrix:
        """
        matrix of the assembled bilinear form
        """
    @property
    def space(self) -> FESpace:
        """
        fespace on which the bilinear form is defined on
        """
class COUPLING_TYPE:
    """
    
    Enum specifying the coupling type of a degree of freedom, each dof is
    either UNUSED_DOF, LOCAL_DOF, INTERFACE_DOF or WIREBASKET_DOF, other values
    are provided as combinations of these:
    
    UNUSED_DOF: Dof is not used, i.e the minion dofs in a Periodic finite
        element space.
    
    LOCAL_DOF: Inner degree of freedom, will be eliminated by static
        condensation and reconstructed afterwards.
    
    HIDDEN_DOF: Inner degree of freedom, that will be eliminated by static
        condensation and *not* reconstruced afterwards(spares some entries).
        Note: 
         * without static condensation a HIDDEN_DOF is treated as any other
           DOF, e.g. as a LOCAL_DOF
         * To a HIDDEN_DOF the r.h.s. vector must have zero entries.
         * When static condensation is applied (eliminate_hidden/
           eliminate_internal) the block corresponding to HIDDEN_DOFs
           has to be invertible.
    
    CONDENSABLE_DOF: Inner degree of freedom, that will be eliminated by static
        condensation (LOCAL_DOF or HIDDEN_DOF)
    
    INTERFACE_DOF: Degree of freedom between two elements, these will not be
        eliminated by static condensation, but not be put into the wirebasket
        system for i.e. a bddc Preconditioner.
    
    NONWIREBASKET_DOF: Either a LOCAL_DOF or an INTERFACE_DOF
    
    WIREBASKET_DOF: Degree of freedom coupling with many elements (more than
        one). These will be put into the system for a bddc preconditioner.
        The HCurl space also treats degrees of freedom of badly shaped
        elements as WIREBASKET_DOFs.
    
    EXTERNAL_DOF: Either INTERFACE_DOF or WIREBASKET_DOF
    
    VISIBLE_DOF: not UNUSED_DOF or HIDDEN_DOF
    
    ANY_DOF: Any used dof (LOCAL_DOF or INTERFACE_DOF or WIREBASKET_DOF)
    
    
    
    Members:
    
      UNUSED_DOF
    
      HIDDEN_DOF
    
      LOCAL_DOF
    
      CONDENSABLE_DOF
    
      INTERFACE_DOF
    
      NONWIREBASKET_DOF
    
      WIREBASKET_DOF
    
      EXTERNAL_DOF
    
      VISIBLE_DOF
    
      ANY_DOF
    """
    ANY_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.ANY_DOF: 15>
    CONDENSABLE_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.CONDENSABLE_DOF: 3>
    EXTERNAL_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.EXTERNAL_DOF: 12>
    HIDDEN_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.HIDDEN_DOF: 1>
    INTERFACE_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.INTERFACE_DOF: 4>
    LOCAL_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.LOCAL_DOF: 2>
    NONWIREBASKET_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.NONWIREBASKET_DOF: 6>
    UNUSED_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.UNUSED_DOF: 0>
    VISIBLE_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.VISIBLE_DOF: 14>
    WIREBASKET_DOF: typing.ClassVar[COUPLING_TYPE]  # value = <COUPLING_TYPE.WIREBASKET_DOF: 8>
    __members__: typing.ClassVar[dict[str, COUPLING_TYPE]]  # value = {'UNUSED_DOF': <COUPLING_TYPE.UNUSED_DOF: 0>, 'HIDDEN_DOF': <COUPLING_TYPE.HIDDEN_DOF: 1>, 'LOCAL_DOF': <COUPLING_TYPE.LOCAL_DOF: 2>, 'CONDENSABLE_DOF': <COUPLING_TYPE.CONDENSABLE_DOF: 3>, 'INTERFACE_DOF': <COUPLING_TYPE.INTERFACE_DOF: 4>, 'NONWIREBASKET_DOF': <COUPLING_TYPE.NONWIREBASKET_DOF: 6>, 'WIREBASKET_DOF': <COUPLING_TYPE.WIREBASKET_DOF: 8>, 'EXTERNAL_DOF': <COUPLING_TYPE.EXTERNAL_DOF: 12>, 'VISIBLE_DOF': <COUPLING_TYPE.VISIBLE_DOF: 14>, 'ANY_DOF': <COUPLING_TYPE.ANY_DOF: 15>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ComponentGridFunction(GridFunction):
    """
    
     Keyword arguments can be:
    multidim: 
     Multidimensional GridFunction
    nested: bool = False
     Generates prolongation matrices for each mesh level and prolongates
     the solution onto the finer grid after a refinement.
    autoupdate: 
     Automatically update on FE space update
    """
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Compress(FESpace):
    """
    Wrapper Finite Element Spaces.
    The compressed fespace is a wrapper around a standard fespace which removes
    certain dofs (e.g. UNUSED_DOFs).
    
    Parameters:
    
    fespace : ngsolve.comp.FESpace
        finite element space
    
    active_dofs : BitArray or None
        don't use the COUPLING_TYPEs of dofs to compress the FESpace, 
        but use a BitArray directly to compress the FESpace
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def GetActiveDofs(self) -> pyngcore.pyngcore.BitArray:
        ...
    def GetBaseSpace(self) -> FESpace:
        ...
    def SetActiveDofs(self, dofs: pyngcore.pyngcore.BitArray) -> None:
        ...
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, fespace: FESpace, active_dofs: typing.Any = ...) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class ContactBoundary:
    def AddEnergy(self, form: ngsolve.fem.CoefficientFunction, deformed: bool = False) -> None:
        ...
    def AddIntegrator(self, form: ngsolve.fem.CoefficientFunction, deformed: bool = False) -> None:
        ...
    def Update(self, gf: GridFunction = None, bf: BilinearForm = None, intorder: int = 4, maxdist: float = 0.0, both_sides: bool = False) -> None:
        """
        Update searchtree for gap function.
        If bf is given add specialelements corresponding to
        integrationrules of order 'intorder' on each master
        element to BilinearForm bf.
        `maxdist` is the maximum distance where this function is accurate.
        If `maxdist` == 0. then 2*meshsize is used.
        """
    def _GetWebguiData(self) -> dict:
        ...
    @typing.overload
    def __init__(self, fes: FESpace, master: Region, minion: Region, draw_pairs: bool = False, volume: bool = False) -> None:
        ...
    @typing.overload
    def __init__(self, master: Region, minion: Region, draw_pairs: bool = False, volume: bool = False) -> None:
        """
        Class for managing contact interfaces.
        The created object must be kept alive in python as long as
        operations of it are used!
        """
    @property
    def gap(self) -> ngsolve.fem.CoefficientFunction:
        ...
    @property
    def normal(self) -> ngsolve.fem.CoefficientFunction:
        ...
class DifferentialSymbol:
    def __call__(self, definedon: Region | str | None = None, element_boundary: bool = False, element_vb: VorB = ..., skeleton: bool = False, bonus_intorder: int = 0, intrules: dict[ngsolve.fem.ET, ngsolve.fem.IntegrationRule] = {}, deformation: GridFunction = None, definedonelements: pyngcore.pyngcore.BitArray = None) -> DifferentialSymbol:
        ...
    def __init__(self, arg0: VorB) -> None:
        ...
class Discontinuous(FESpace, NGS_Object):
    """
    Discontinuous Finite Element Spaces.
    FESpace that splits up all dofs that are shared by several (volume or surface) elements. Every element gets a single copy of that dof. Basis functions become element-local.
    
    Parameters:
    
    fespace : ngsolve.comp.FESpace
        finite element space
    
    BND : boolean or None
        separate across surface elements instead of volume elements (for surface FESpaces)
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, fespace: FESpace, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class DualProxyFunction(ProxyFunction):
    def __call__(self, arg0: ngsolve.fem.CoefficientFunction) -> ...:
        ...
class ElementId:
    """
    
    An element identifier containing element number and Volume/Boundary flag
    
    3 __init__ overloads:
    
    1)
    
    Parameters:
    
    vb : ngsolve.comp.VorB
      input Volume or Boundary (VOL, BND, BBND, BBBND)
    
    nr : int
      input element number
    
    
    2)
    
    Parameters:
    
    nr : int
      input element number
    
    
    3)
    
    Parameters:
    
    el : ngcomp::Ngs_Element
      input Ngs element
    
    """
    def VB(self) -> VorB:
        """
        VorB of element
        """
    def __eq__(self, arg0: ElementId) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    @typing.overload
    def __init__(self, vb: VorB, nr: int) -> None:
        ...
    @typing.overload
    def __init__(self, nr: int) -> None:
        ...
    @typing.overload
    def __init__(self, el: ...) -> None:
        ...
    def __ne__(self, arg0: ElementId) -> bool:
        ...
    def __str__(self) -> str:
        ...
    @property
    def nr(self) -> int:
        """
        the element number
        """
    @property
    def valid(self) -> bool:
        """
        is element valid
        """
class ElementRange(ngsolve.ngstd.IntRange):
    def __init__(self, mesh: Mesh, vb: VorB, range: ngsolve.ngstd.IntRange) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Ngs_Element]:
        ...
class FESpace(NGS_Object):
    """
    Finite Element Space
    
    Provides the functionality for finite element calculations.
    
    Some available FESpaces are:
    
    H1, HCurl, HDiv, L2, FacetFESpace, HDivDiv
    
    2 __init__ overloads:
      1) To create a registered FESpace
      2) To create a compound FESpace from multiple created FESpaces
    
    1)
    
    Parameters:
    
    type : string
      Type of the finite element space. This parameter is automatically
      set if the space is constructed with a generator function.
    
    mesh : ngsolve.Mesh
      Mesh on which the finite element space is defined on.
    
    kwargs : kwargs
      For a description of the possible kwargs have a look a bit further down.
    
    2)
    
    Parameters:
    
    spaces : list of ngsolve.FESpace
      List of the spaces for the compound finite element space
    
    kwargs : kwargs
      For a description of the possible kwargs have a look a bit further down.
    
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    @staticmethod
    def __special_treated_flags__() -> dict:
        ...
    def ApplyM(self, vec: ngsolve.la.BaseVector, rho: ngsolve.fem.CoefficientFunction = None, definedon: Region = None) -> None:
        """
        Apply mass-matrix. Available only for L2-like spaces
        """
    def ConvertL2Operator(self, l2space: FESpace) -> BaseMatrix:
        ...
    def CouplingType(self, dofnr: int) -> COUPLING_TYPE:
        """
                 Get coupling type of a degree of freedom.
        
        Parameters:
        
        dofnr : int
          input dof number
        """
    def CreateDirectSolverCluster(self, **kwargs) -> list:
        ...
    def CreateSmoothingBlocks(self, **kwargs) -> pyngcore.pyngcore.Table_I:
        """
        Create table of smoothing blocks for block-Jacobi/block-Gauss-Seidel preconditioners.
        
        Every table entry describes the set of dofs belonging a Jacobi/Gauss-Seidel block.
        
        Paramters:
        
        blocktype: string | [ string ] | int
            describes blocktype.
            string form ["vertex", "edge", "face",  "facet", "vertexedge", ....]
            or list of strings for combining multiple blocktypes
            int is for backward compatibility with old style blocktypes
        
        condense: bool = False
            exclude dofs eliminated by static condensation
        """
    @typing.overload
    def Elements(self, VOL_or_BND: VorB = ...) -> FESpaceElementRange:
        """
        Returns an iterable range of elements.
        
        Parameters:
        
        VOL_or_BND : ngsolve.comp.VorB
          input VOL, BND, BBND,...
        """
    @typing.overload
    def Elements(self, arg0: Region) -> typing.Iterator[FESpaceElement]:
        ...
    def FinalizeUpdate(self) -> None:
        """
        finalize update
        """
    def FreeDofs(self, coupling: bool = False) -> pyngcore.pyngcore.BitArray:
        """
        Return BitArray of free (non-Dirichlet) dofs\\n
        coupling=False ... all free dofs including local dofs\\n
        coupling=True .... only element-boundary free dofs
        
        Parameters:
        
        coupling : bool
          input coupling
        """
    @typing.overload
    def GetDofNrs(self, ei: ElementId) -> tuple:
        """
        Parameters:
        
        ei : ngsolve.comp.ElementId
          input element id
        """
    @typing.overload
    def GetDofNrs(self, ni: NodeId) -> tuple:
        """
        Parameters:
        
        ni : ngsolve.comp.NodeId
          input node id
        """
    def GetDofs(self, region: Region) -> pyngcore.pyngcore.BitArray:
        """
        Returns all degrees of freedom in given region.
        
        Parameters:
        
        region : ngsolve.comp.Region
          input region
        """
    def GetFE(self, ei: ElementId) -> typing.Any:
        """
        Get the finite element to corresponding element id.
        
        Parameters:
        
        ei : ngsolve.comp.ElementId
           input element id
        """
    def GetOrder(self, nodeid: NodeId) -> int:
        """
        return order of node.
        by now, only isotropic order is supported here
        """
    def GetTrace(self, arg0: FESpace, arg1: ngsolve.la.BaseVector, arg2: ngsolve.la.BaseVector, arg3: bool) -> None:
        ...
    def GetTraceTrans(self, arg0: FESpace, arg1: ngsolve.la.BaseVector, arg2: ngsolve.la.BaseVector, arg3: bool) -> None:
        ...
    def HideAllDofs(self, component: typing.Any = ...) -> None:
        """
        set all visible coupling types to HIDDEN_DOFs (will be overwritten by any Update())
        """
    def InvM(self, rho: ngsolve.fem.CoefficientFunction = None) -> BaseMatrix:
        ...
    def Mass(self, rho: ngsolve.fem.CoefficientFunction = None, definedon: Region | None = None) -> BaseMatrix:
        ...
    def ParallelDofs(self) -> ngsolve.la.ParallelDofs:
        """
        Return dof-identification for MPI-distributed meshes
        """
    def Prolongation(self) -> ...:
        """
        Return prolongation operator for use in multi-grid
        """
    def Range(self, arg0: int) -> ngsolve.la.DofRange:
        """
        deprecated, will be only available for ProductSpace
        """
    @typing.overload
    def SetCouplingType(self, dofnr: int, coupling_type: COUPLING_TYPE) -> None:
        """
                 Set coupling type of a degree of freedom.
        
        Parameters:
        
        dofnr : int
          input dof number
        
        coupling_type : ngsolve.comp.COUPLING_TYPE
          input coupling type
        """
    @typing.overload
    def SetCouplingType(self, dofnrs: ngsolve.ngstd.IntRange, coupling_type: COUPLING_TYPE) -> None:
        """
                 Set coupling type for interval of dofs.
        
        Parameters:
        
        dofnrs : Range
          range of dofs
        
        coupling_type : ngsolve.comp.COUPLING_TYPE
          input coupling type
        """
    def SetDefinedOn(self, region: Region) -> None:
        """
        Set the regions on which the FESpace is defined.
        
        Parameters:
        
        region : ngsolve.comp.Region
          input region
        """
    @typing.overload
    def SetOrder(self, element_type: ngsolve.fem.ET, order: int) -> None:
        """
        Parameters:
        
        element_type : ngsolve.fem.ET
          input element type
        
        order : object
          input polynomial order
        """
    @typing.overload
    def SetOrder(self, nodeid: NodeId, order: int) -> None:
        """
        Parameters:
        
        nodeid : ngsolve.comp.NodeId
          input node id
        
        order : int
          input polynomial order
        """
    def SolveM(self, vec: ngsolve.la.BaseVector, rho: ngsolve.fem.CoefficientFunction = None, definedon: Region = None) -> None:
        """
                 Solve with the mass-matrix. Available only for L2-like spaces.
        
        Parameters:
        
        vec : ngsolve.la.BaseVector
          input right hand side vector
        
        rho : ngsolve.fem.CoefficientFunction
          input CF
        """
    def TestFunction(self) -> typing.Any:
        """
        Return a proxy to be used as a testfunction for Symbolic Integrators
        """
    def TnT(self) -> tuple[typing.Any, typing.Any]:
        """
        Return a tuple of trial and testfunction
        """
    def TraceOperator(self, tracespace: FESpace, average: bool) -> BaseMatrix:
        ...
    def TrialFunction(self) -> typing.Any:
        """
        Return a proxy to be used as a trialfunction in Symbolic Integrators
        """
    def Update(self) -> None:
        """
        update space after mesh-refinement
        """
    def UpdateDofTables(self) -> None:
        """
        update dof-tables after changing polynomial order distribution
        """
    def __eq__(self, space: FESpace) -> bool:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, spaces: list, **kwargs) -> None:
        """
        construct product space (compound-space) from list of component spaces
        """
    @typing.overload
    def __init__(self, type: str, mesh: Mesh, **kwargs) -> None:
        """
        allowed types are: 'h1ho', 'l2ho', 'hcurlho', 'hdivho' etc.
        """
    def __mul__(self, arg0: FESpace) -> ...:
        ...
    def __pow__(self, arg0: int) -> ...:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __timing__(self) -> typing.Any:
        ...
    @property
    def autoupdate(self) -> bool:
        ...
    @property
    def components(self) -> tuple:
        """
        deprecated, will be only available for ProductSpace
        """
    @property
    def couplingtype(self) -> FlatArray_N6ngcomp13COUPLING_TYPEE_S:
        ...
    @property
    def dim(self) -> int:
        """
        multi-dim of FESpace
        """
    @property
    def globalorder(self) -> int:
        """
        query global order of space
        """
    @property
    def is_complex(self) -> bool:
        ...
    @property
    def loembedding(self) -> BaseMatrix:
        ...
    @property
    def lospace(self) -> FESpace:
        ...
    @property
    def mesh(self) -> Mesh:
        """
        mesh on which the FESpace is created
        """
    @property
    def ndof(self) -> int:
        """
        number of degrees of freedom
        """
    @property
    def ndofglobal(self) -> int:
        """
        global number of dofs on MPI-distributed mesh
        """
    @property
    def type(self) -> str:
        """
        type of finite element space
        """
class FESpaceElement(Ngs_Element):
    def GetFE(self) -> ngsolve.fem.FiniteElement:
        """
        the finite element containing shape functions
        """
    def GetTrafo(self) -> ngsolve.fem.ElementTransformation:
        """
        the transformation from reference element to physical element
        """
    @property
    def dofs(self) -> list:
        """
        degrees of freedom of element
        """
class FESpaceElementRange(ngsolve.ngstd.IntRange):
    def __iter__(self) -> typing.Iterator[...]:
        ...
class FacetFESpace(FESpace):
    """
    A finite element space living on facets.
    
    The FacetFESpace provides polynomials on facets, i.e. faces in 3D,
    edges in 2D, and vertices in 1D. The functions are discontinuous from facet to facet.
    
    Typecal usecases for the FacetFESpace are hybrid mixed and hybrid DG methods.
    
    The function is only defined on the mesh skeleton. Evaluation inside the element throws
    an exception. Thus, functions from the FacetFESpace can be used only within element_boundary 
    or skeleton expressions. 
    
    Functions have meaningful boundary-values, which are obtained using the Trace-operator.
    (the trace operator might become redundant in future).
    
    (coming soon) The FacetFESpace provides variable order, which can be set for FACET-nodes. Alternatively,
    one can use FACE, EDGE, or VERTEX nodes for 3D, 2D, or 1D meshes, respectively.
    
    The basis is L2-orthogonal on the facets. The highest order basis functions can be duplicated
    for the two neighbouring elements. This allows a simple implementation of the Lehrenfeld-Schoeberl
    'projected jumps' HDG method.
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    highest_order_dc: bool = False
      Splits highest order facet functions into two which are associated with
      the corresponding neighbors and are local dofs on the corresponding element
      (used to realize projected jumps)
    hide_highest_order_dc: bool = False
      if highest_order_dc is used this flag marks the corresponding local dofs
      as hidden dofs (reduces number of non-zero entries in a matrix). These dofs
      can also be compressed.
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class FacetSurface(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class FlatArray_N6ngcomp13COUPLING_TYPEE_S:
    def NumPy(self) -> typing.Any:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: int) -> COUPLING_TYPE:
        ...
    def __iter__(self) -> typing.Iterator[COUPLING_TYPE]:
        ...
    def __len__(self) -> int:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: COUPLING_TYPE) -> COUPLING_TYPE:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: COUPLING_TYPE) -> None:
        ...
    def __str__(self) -> str:
        ...
class GlobalInterfaceSpace(FESpace):
    """
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __init__(self, mesh: Mesh, mapping: ngsolve.fem.CoefficientFunction, definedon: Region | None = None, periodic: bool = False, periodicu: bool = False, periodicv: bool = False, order: int = 3, complex: bool = False, polar: bool = False, autoupdate: bool = False) -> None:
        ...
class GlobalSpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    basis: Basis functions.
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    @staticmethod
    def __special_treated_flags__() -> dict:
        ...
    def AddOperator(self, arg0: str, arg1: VorB, arg2: ngsolve.fem.CoefficientFunction) -> None:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class GlobalVariables:
    numthreads: int
    @property
    def code_uses_tensors(self) -> bool:
        """
        Use tensors in code-generation
        """
    @code_uses_tensors.setter
    def code_uses_tensors(self, arg1: bool) -> None:
        ...
    @property
    def msg_level(self) -> int:
        """
        message level
        """
    @msg_level.setter
    def msg_level(self, arg1: int) -> None:
        ...
    @property
    def pajetrace(self) -> str:
        ...
    @pajetrace.setter
    def pajetrace(self, arg1: int) -> None:
        ...
    @property
    def symbolic_integrator_uses_diff(self) -> bool:
        """
        New treatment of symobolic forms using differentiation by proxies
        """
    @symbolic_integrator_uses_diff.setter
    def symbolic_integrator_uses_diff(self, arg1: bool) -> None:
        ...
    @property
    def testout(self) -> str:
        """
        testout file
        """
    @testout.setter
    def testout(self, arg1: str) -> None:
        ...
class GridFunction(ngsolve.fem.CoefficientFunction):
    """
    a field approximated in some finite element space
     Keyword arguments can be:
    multidim: 
     Multidimensional GridFunction
    nested: bool = False
     Generates prolongation matrices for each mesh level and prolongates
     the solution onto the finer grid after a refinement.
    autoupdate: 
     Automatically update on FE space update
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def AddMultiDimComponent(self, arg0: ngsolve.la.BaseVector) -> None:
        ...
    def CF(self, diffop: ngsolve.fem.DifferentialOperator) -> ngsolve.fem.CoefficientFunction:
        """
        Parameters:
        
        diffop : ngsolve.fem.DifferentialOperator
          input differential operator
        """
    def Deriv(self) -> ngsolve.fem.CoefficientFunction:
        """
        Returns the canonical derivative of the space behind the GridFunction if possible.
        """
    def Interpolate(self, coefficient: ngsolve.fem.CoefficientFunction, definedon: typing.Any = ..., mdcomp: int = 0) -> None:
        ...
    def Load(self, filename: str, parallel: bool = False) -> None:
        """
        Loads a gridfunction from a file.
        
        Parameters:
        
        filename : string
          input file name
        
        parallel : bool
          input parallel
        """
    def MDComponent(self, mdcomp: int) -> GridFunctionCoefficientFunction:
        """
        select component of multidim GridFunction
        """
    def Operator(self, name: str, VOL_or_BND: VorB = ...) -> GridFunctionCoefficientFunction:
        """
        Get access to an operator depending on the FESpace.
        
        Parameters:
        
        name : string
          input name of the requested operator
        
        VOL_or_BND : ngsolve.comp.VorB
          input VOL, BND, BBND, ...
        """
    def Operators(self) -> list:
        """
        returns list of available differential operators
        """
    def Save(self, filename: str, parallel: bool = False) -> None:
        """
        Saves the gridfunction into a file.
        
        Parameters:
        
        filename : string
          input file name
        
        parallel : bool
          input parallel
        """
    def Set(self, coefficient: ngsolve.fem.CoefficientFunction, VOL_or_BND: VorB = ..., definedon: typing.Any = ..., dual: bool = False, use_simd: bool = True, mdcomp: int = 0, definedonelements: pyngcore.pyngcore.BitArray | None = None, bonus_intorder: int = 0) -> None:
        """
        Set values
        
        Parameters:
        
        coefficient : ngsolve.fem.CoefficientFunction
          input CF to set
        
        VOL_or_BND : ngsolve.comp.VorB
          input VOL, BND, BBND, ...
        
        definedon : object
          input definedon region
        
        dual : bool
          If set to true dual shapes are used, otherwise local L2-projection is used.
          Default is False.
        
        use_simd : bool
          If set to false does not use SIMD (for debugging).
        
        mdcomp : int
          .
        
        definedonelements : nullopt
          .
        
        bonus_intorder : int
          Increase numerical integration order.
        """
    def Trace(self) -> GridFunctionCoefficientFunction:
        """
        take canonical boundary trace. This function is optional, added for consistency with proxies
        """
    def Update(self) -> None:
        """
        update vector size to finite element space dimension after mesh refinement
        """
    @typing.overload
    def __call__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, VOL_or_BND: VorB = ...) -> typing.Any:
        ...
    @typing.overload
    def __call__(self, *args, **kwargs) -> typing.Any:
        ...
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, space: FESpace, name: str = 'gfu', **kwargs) -> None:
        """
        creates a gridfunction in finite element space
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def autoupdate(self) -> bool:
        ...
    @property
    def components(self) -> tuple:
        """
        list of gridfunctions for compound gridfunction
        """
    @property
    def derivname(self) -> str:
        """
        Name of canonical derivative of the space behind the GridFunction.
        """
    @property
    def name(self) -> str:
        """
        Name of the Gridfunction
        """
    @property
    def space(self) -> FESpace:
        """
        the finite element space
        """
    @property
    def vec(self) -> ngsolve.la.BaseVector:
        """
        coefficient vector
        """
    @property
    def vecs(self) -> ngsolve.la.MultiVector:
        """
        list of coefficient vectors for multi-dim gridfunction
        """
class GridFunctionC(GridFunction):
    """
    
     Keyword arguments can be:
    multidim: 
     Multidimensional GridFunction
    nested: bool = False
     Generates prolongation matrices for each mesh level and prolongates
     the solution onto the finer grid after a refinement.
    autoupdate: 
     Automatically update on FE space update
    """
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class GridFunctionCoefficientFunction(ngsolve.fem.CoefficientFunction):
    def Trace(self) -> GridFunctionCoefficientFunction:
        """
        take canonical boundary trace.
        """
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class GridFunctionD(GridFunction):
    """
    
     Keyword arguments can be:
    multidim: 
     Multidimensional GridFunction
    nested: bool = False
     Generates prolongation matrices for each mesh level and prolongates
     the solution onto the finer grid after a refinement.
    autoupdate: 
     Automatically update on FE space update
    """
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class H1(FESpace):
    """
    An H1-conforming finite element space.
    
    The H1 finite element space consists of continuous and
    element-wise polynomial functions. It uses a hierarchical (=modal)
    basis built from integrated Legendre polynomials on tensor-product elements,
    and Jaboci polynomials on simplicial elements. 
    
    Boundary values are well defined. The function can be used directly on the
    boundary, using the trace operator is optional.
    
    The H1 space supports variable order, which can be set individually for edges, 
    faces and cells. 
    
    Internal degrees of freedom are declared as local dofs and are eliminated 
    if static condensation is on.
    
    The wirebasket consists of all vertex dofs. Optionally, one can include the 
    first (the quadratic bubble) edge basis function, or all edge basis functions
    into the wirebasket.
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    wb_withedges: bool = true(3D) / false(2D)
      use lowest-order edge dofs for BDDC wirebasket
    wb_fulledges: bool = false
      use all edge dofs for BDDC wirebasket
    hoprolongation: bool = false
      (experimental, only trigs) creates high order prolongation,
      and switches off low-order space
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class H1LumpingFESpace(FESpace):
    """
    H1-FESpace with nodal basis for mass lumping.
    
    at the moment only for second order + bub on trigs.
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def GetIntegrationRules(self) -> dict[ngsolve.fem.ET, ngsolve.fem.IntegrationRule]:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HCurl(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    nograds: bool = False
      Remove higher order gradients of H1 basis functions from HCurl FESpace
    type1: bool = False
      Use type 1 Nedelec elements
    discontinuous: bool = False
      Create discontinuous HCurl space
    gradientdomains: List[int] = None
      Remove high order gradients from domains where the value is 0.
      This list can be generated for example like this:
      graddoms = [1 if mat == 'iron' else 0 for mat in mesh.GetMaterials()]
    gradientboundaries: List[int] = None
      Remove high order gradients from boundaries where the value is 0.
      This list can be generated for example like this:
      gradbnds = [1 if bnd == 'iron_bnd' else 0 for bnd in mesh.GetBoundaries()]
    highest_order_dc: bool = False
      Activates relaxed H(curl)-conformity. Allows tangential discontinuity of highest order edge basis functions
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def CreateGradient(self) -> tuple:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HCurlAMG(Preconditioner):
    """
    
     Keyword arguments can be:
    inverse: 
      Inverse type used in Preconditioner.
    test: bool = False
      Computes condition number for preconditioner, if testout file
      is set, prints eigenvalues to file.
    block: 
      use block-Jacobi/block-Gauss-Seidel
    blocktype: 
      blocktype like 'vertexpatch', 'edgepatch', ...
    """
    def __init__(self, bf: BilinearForm, **kwargs) -> None:
        ...
class HCurlCurl(FESpace):
    """
    A Regge finite element space.
    
    The Regge finite element space consists of element-wise symmetric matrix-valued polynomial functions with tangential-tangential continuity over element interfaces. The normal-tangential (tangential-normal) and normal-normal components can jump over elements.
    
    Tangential-tangential boundary values are well defined.
    
    Several (nonlinear) differential operators from differential geometry are implemented for Regge elements. For all curvature related objects we use the sign convention of Lee " Introduction to Riemannian manifolds".
    curl: Row-wise curl of Regge element
    grad: Gradient of Regge element
    inc: incompatibility operator
         inc(g) = d_1d_1 g_22 - 2*d_1d_2 g_12 + d_2d_2 g_11 in 2D
         inc(g) = curl(Trans(curl(g))) in 3D
    christoffel: Computes the Christoffel symbol of first kind, which is a third-order tensor: Gamma_ijk(g) = 0.5*(d_i g_jk + d_j g_ik - d_k g_ij)
    christoffel2: Computes the Christoffel symbol of second kind, which is a nonlinear third-order tensor: Gamma_ij^k(g) = Inv(g)^kp Gamma_ijp(g)
    Riemann: Computes the fourth-order Riemann curvature tensor. 
             R(X,Y)Z = nabla_X nabla_Y Z - nabla_Y nabla_X Z-nabla_[X,Y] Z
             R_ijkl(g) = d_i Gamma_jkl(g) - d_j Gamma_ikl(g) + Gamma_ik^p(g) Gamma_jlp(g) - Gamma_jk^p(g) Gamma_ilp(g)
    curvature: Curvature operator Q(X wedge Y, W wedge Z) = R(X,Y,Z,W)
               Q = R1221 in 2D
               Q(e_i x e_j, e_l x e_k) = R_ijkl in 3D
    Ricci: Ricci curvature tensor Ric_ij(g) = R_iklj(g) Inv(g)^kl
    scalar: Scalar curvature S(g) = Ric_ij(g) Inv(g)^ij = R_iklj(g) Inv(g)^kl Inv(g)^ij
    Einstein: Einstein tensor Ein_ij(g) = Ric_ij(g)-0.5*S(g) g_ij
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    discontinuous: bool = False
      Create discontinuous HCurlCurl space
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HCurlDiv(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    discontinuous: bool = false
      Create discontinuous HCurlDiv space
    ordertrace: int = -1
      Set order of trace bubbles
    orderinner: int = -1
      Set order of inner nt-bubbles
    GGbubbles: bool = false
      Add GG-bubbles for weak-symmetric formulation
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HDiv(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    RT: bool = False
      RT elements for simplicial elements: P^k subset RT_k subset P^{k+1}
    discontinuous: bool = False
      Create discontinuous HDiv space
    hodivfree: bool = False
      Remove high order element bubbles with non zero divergence
    highest_order_dc: bool = False
      Activates relaxed H(div)-conformity. Allows normal discontinuity of highest order facet basis functions
    hide_all_dofs: bool = False
      Set all used dofs to HIDDEN_DOFs
    orderinner: int = unused
      Set order of inner shapes (orderinner=0 for no inner shapes)
    
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def Average(self, vector: ngsolve.la.BaseVector) -> None:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HDivDiv(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    discontinuous: bool = False
      Create discontinuous HDivDiv space
    plus: bool = False
      Add additional internal element bubble
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HDivDivSurface(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    discontinuous: bool = False
      Create discontinuous HDivDiv space
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class HDivSurface(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    discontinuous: bool = False
      Create discontinuous HDivSurface space
    hodivfree: bool = False
      Remove high order element bubbles with non zero divergence
    RT: bool = False
      RT elements for simplicial elements: P^k subset RT_k subset P^{k+1}
    orderinner: optional<int> = undefined
      order for inner space if defined, otherwise use order for orderinner
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def Average(self, vector: ngsolve.la.BaseVector) -> None:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Hidden(FESpace, NGS_Object):
    """
    Hidden Finite Element Spaces.
    FESpace has elements, but no gobally enumerated dofs, i.e. all dofs are hidden.
    
    Parameters:
    
    fespace : ngsolve.comp.FESpace
        finite element space
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __init__(self, fespace: FESpace, **kwargs) -> None:
        ...
class Integral:
    def MakeBFI(self) -> ngsolve.fem.BFI:
        ...
    def MakeLFI(self) -> ngsolve.fem.LFI:
        ...
    def __radd__(self, arg0: int) -> ...:
        ...
    @property
    def coef(self) -> ngsolve.fem.CoefficientFunction:
        ...
    @property
    def symbol(self) -> DifferentialSymbol:
        ...
class IntegrationRuleSpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def GetIntegrationRules(self) -> dict[ngsolve.fem.ET, ngsolve.fem.IntegrationRule]:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class IntegrationRuleSpaceSurface(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def GetIntegrationRules(self) -> dict[ngsolve.fem.ET, ngsolve.fem.IntegrationRule]:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class InterpolateProxy(ProxyFunction):
    pass
class L2(FESpace):
    """
    An L2-conforming finite element space.
    
    The L2 finite element space consists of element-wise polynomials,
    which are discontinuous from element to element. It uses an
    L2-orthogonal hierarchical basis which leads to orthogonal
    mass-matrices on non-curved elements.
    
    Boundary values are not meaningful for an L2 function space.
    
    The L2 space supports element-wise variable order, which can be set
    for ELEMENT-nodes.
    
    Per default, all dofs are local dofs and are condensed if static
    condensation is performed. The lowest order can be kept in the
    WIRE_BASKET via the flag 'lowest_order_wb=True'.
    
    All dofs can be hidden. Then the basis functions don't show up in the
    global system.
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    all_dofs_together: bool = True
      Change ordering of dofs. If this flag ist set,
      all dofs of an element are ordered successively.
      Otherwise, the lowest order dofs (the constants)
      of all elements are ordered first.
    lowest_order_wb: bool = False
      Keep lowest order dof in WIRE_BASKET
    hide_all_dofs: bool = False
      Set all used dofs to HIDDEN_DOFs
    tp: bool = False
      Use sum-factorization for evaluation
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class LinearForm(NGS_Object):
    """
    
    Used to store the left hand side of a PDE. Add integrators
    (ngsolve.LFI) to it to implement your PDE.
    
    Parameters:
    
    space : ngsolve.FESpace
      The space the linearform is defined on. Can be a compound
      FESpace for a mixed formulation.
    
    flags : dict
      Additional options for the linearform, for example:
    
        print : bool
          Write additional debug information to testout file. This
          file must be set by ngsolve.SetTestoutFile. Use
          ngsolve.SetNumThreads(1) for serial output.
    
    
     Keyword arguments can be:
    print: bool
      Write additional debug information to testout file.
      This file must be set by ngsolve.SetTestoutFile. Use
      ngsolve.SetNumThreads(1) for serial output.
    printelvec: bool
      print element vectors to testout file
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    @typing.overload
    def Add(self, integrator: ngsolve.fem.LFI) -> LinearForm:
        """
        Add integrator to linear form.
        
        Parameters:
        
        integrator : ngsolve.fem.LFI
          input linear form integrator
        """
    @typing.overload
    def Add(self, arg0: SumOfIntegrals) -> typing.Any:
        ...
    def Assemble(self) -> LinearForm:
        """
        Assemble linear form
        """
    def __call__(self, gf: GridFunction) -> float:
        ...
    @typing.overload
    def __iadd__(self, lfi: ngsolve.fem.LFI) -> LinearForm:
        ...
    @typing.overload
    def __iadd__(self, lfi: ngsolve.fem.PointEvaluationFunctional) -> LinearForm:
        ...
    @typing.overload
    def __iadd__(self, arg0: SumOfIntegrals) -> LinearForm:
        ...
    @typing.overload
    def __init__(self, space: FESpace, **kwargs) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: SumOfIntegrals, **kwargs) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def components(self) -> list:
        """
        list of components for linearforms on compound-space
        """
    @property
    def integrators(self) -> tuple:
        """
        returns tuple of integrators of the linear form
        """
    @property
    def space(self) -> FESpace:
        ...
    @property
    def vec(self) -> ngsolve.la.BaseVector:
        """
        vector of the assembled linear form
        """
class LocalPreconditioner(Preconditioner):
    """
    A local preconditioner.
    
    additive or multiplicative point or block preconditioner
    
    Keyword arguments can be:
    
    block: bool = false
      use block Jacobi/Gauss-Seidel
    GS: bool = false
      use Gauss-Seidel instead of Jacobi
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __init__(self, bf: BilinearForm, **kwargs) -> None:
        ...
class MatrixValued(ProductSpace):
    """
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __init__(self, space: FESpace, dim: int | None = None, symmetric: bool = False, deviatoric: bool = False, skewsymmetric: bool = False, autoupdate: bool = False) -> None:
        ...
class Mesh:
    """
    
    NGSolve interface to the Netgen mesh. Provides access and functionality
    to use the mesh for finite element calculations.
    
    Parameters:
    
    mesh (netgen.Mesh): a mesh generated from Netgen
    
    
    """
    __hash__: typing.ClassVar[None] = None
    def BBBoundaries(self, pattern: str) -> Region:
        """
        Return co dim 3 boundary mesh-region matching the given regex pattern
        """
    def BBoundaries(self, pattern: str) -> Region:
        """
        Return co dim 2 boundary mesh-region matching the given regex pattern
        """
    @typing.overload
    def Boundaries(self, pattern: str) -> Region:
        """
        Return boundary mesh-region matching the given regex pattern
        """
    @typing.overload
    def Boundaries(self, bnds: list[int]) -> Region:
        """
        Generate boundary mesh-region by boundary condition numbers
        """
    def BoundaryCF(self, values: dict, default: ngsolve.fem.CoefficientFunction = None) -> ngsolve.fem.CoefficientFunction:
        """
        Boundary wise CoefficientFunction.
        First argument is a dict from either boundary names or Region objects to
        CoefficientFunction (-values). Later given names/regions override earlier
        values. Optional last argument (default) is the value for not given boundaries.
        >>> penalty = mesh.BoundaryCF({ "top" : 1e6 }, default=0)
        will create a CF being 1e6 on the top boundary and 0. elsewhere.
        """
    def BuildRefinementTree(self) -> pyngcore.pyngcore.Array_y_S:
        ...
    def Contains(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> bool:
        """
        Check if the point (x,y,z) is in the meshed domain (is inside a volume element)
        """
    def Curve(self, order: int) -> Mesh:
        """
        Curve the mesh elements for geometry approximation of given order
        """
    def Elements(self, VOL_or_BND: VorB = ...) -> ...:
        """
        Return an iterator over elements on VOL/BND
        """
    def GeoParamCF(self) -> ngsolve.fem.CoefficientFunction:
        ...
    def GetBBBoundaries(self) -> tuple:
        """
        Return list of boundary conditions for co dimension 3
        """
    def GetBBoundaries(self) -> tuple:
        """
        Return list of boundary conditions for co dimension 2
        """
    def GetBoundaries(self) -> tuple:
        """
        Return list of boundary condition names
        """
    def GetCurveOrder(self) -> int:
        ...
    def GetHPElementLevel(self, ei: ElementId) -> int:
        """
        THIS FUNCTION IS WIP!
         Return HP-refinement level of element
        """
    def GetMaterials(self) -> tuple:
        """
        Return list of material names
        """
    def GetNE(self, arg0: VorB) -> int:
        """
        Return number of elements of codimension VorB.
        """
    def GetPMLTrafo(self, dom: int = 1) -> pml.PML:
        """
        Return pml transformation on domain dom
        """
    def GetPMLTrafos(self) -> list:
        """
        Return list of pml transformations
        """
    def GetParentElement(self, ei: ElementId) -> ElementId:
        """
        Return parent element id on refined mesh
        """
    def GetParentFaces(self, fnum: int) -> tuple:
        """
        Return parent faces
        """
    def GetParentVertices(self, vnum: int) -> tuple:
        """
        Return parent vertex numbers on refined mesh
        """
    def GetPeriodicNodePairs(self, arg0: ngsolve.fem.NODE_TYPE) -> list:
        """
        returns list of periodic nodes with their identification number as [((master_nr, minion_nr),idnr),...]
        """
    def GetTrafo(self, eid: ElementId) -> ngsolve.fem.ElementTransformation:
        """
        returns element transformation of given element id
        """
    def LocalHCF(self) -> ngsolve.fem.CoefficientFunction:
        ...
    @typing.overload
    def MapToAllElements(self, arg0: ngsolve.fem.IntegrationRule, arg1: VorB | Region) -> numpy.ndarray[ngsolve.fem.MeshPoint]:
        ...
    @typing.overload
    def MapToAllElements(self, arg0: dict[ngsolve.fem.ET, ngsolve.fem.IntegrationRule], arg1: VorB | Region) -> numpy.ndarray[ngsolve.fem.MeshPoint]:
        ...
    def MaterialCF(self, values: dict, default: ngsolve.fem.CoefficientFunction = None) -> ngsolve.fem.CoefficientFunction:
        """
        Domain wise CoefficientFunction.
        First argument is a dict from either material names or Region objects to
        CoefficientFunction (-values). Later given names/regions override earlier
        values. Optional last argument (default) is the value for not given materials.
        >>> sigma = mesh.MaterialCF({ "steel_.*" : 2e6 }, default=0)
        will create a CF being 2e6 on all domains starting with 'steel_' and 0 elsewhere.
        """
    @typing.overload
    def Materials(self, pattern: str) -> Region:
        """
        Return mesh-region matching the given regex pattern
        """
    @typing.overload
    def Materials(self, domains: list[int]) -> Region:
        """
        Generate mesh-region by domain numbers
        """
    def Refine(self, mark_surface_elements: bool = False, onlyonce: bool = False) -> None:
        """
        Local mesh refinement based on marked elements, uses element-bisection algorithm
        """
    def RefineFromTree(self, arg0: pyngcore.pyngcore.Array_y_S) -> None:
        ...
    def RefineHP(self, levels: int, factor: float = 0.125) -> None:
        """
        Geometric mesh refinement towards marked vertices and edges, uses factor for placement of new points
        """
    def Region(self, vb: VorB, pattern: str | None = '.*') -> Region:
        """
        Return boundary mesh-region matching the given regex pattern
        """
    def RegionCF(self, VorB: VorB, value: dict, default: ngsolve.fem.CoefficientFunction = None) -> ngsolve.fem.CoefficientFunction:
        """
        Region wise CoefficientFunction.
        First argument is VorB, defining the co-dimension,
        second argument is a dict from either region names or Region objects to
        CoefficientFunction (-values). Later given names/regions override earlier
        values. Optional last argument (default) is the value for not given regions.
        >>> sigma = mesh.RegionCF(VOL, { "steel_.*" : 2e6 }, default=0)
        will create a CF being 2e6 on all domains starting with 'steel_' and 0 elsewhere.
        """
    def SetDeformation(self, gf: ...) -> None:
        """
        Deform the mesh with the given GridFunction
        """
    def SetElementOrder(self, eid: ElementId, order: int) -> None:
        """
        For backward compatibility, not recommended to use
        """
    def SetPML(self, pmltrafo: pml.PML, definedon: typing.Any) -> None:
        """
        Set PML transformation on domain
        """
    def SetRefinementFlag(self, ei: ElementId, refine: bool) -> None:
        """
        Set refinementflag for mesh-refinement
        """
    def SetRefinementFlags(self, refine: list[bool]) -> None:
        """
        Set refinementflags for mesh-refinement
        """
    def SplitElements_Alfeld(self) -> None:
        ...
    def UnSetPML(self, definedon: typing.Any) -> None:
        """
        Unset PML transformation on domain
        """
    def UnsetDeformation(self) -> None:
        """
        Unset the deformation
        """
    def __call__(self, x: numpy.ndarray[numpy.float64] = 0.0, y: numpy.ndarray[numpy.float64] = 0.0, z: numpy.ndarray[numpy.float64] = 0.0, VOL_or_BND: VorB = ...) -> typing.Any:
        """
        Get a MappedIntegrationPoint in the point (x,y,z) on the matching volume (VorB=VOL, default) or surface (VorB=BND) element. BBND elements aren't supported
        """
    def __eq__(self, mesh: Mesh) -> bool:
        ...
    @typing.overload
    def __getitem__(self, arg0: ElementId) -> Ngs_Element:
        """
        Return Ngs_Element from given ElementId
        """
    @typing.overload
    def __getitem__(self, arg0: NodeId) -> MeshNode:
        """
        Return MeshNode from given NodeId
        """
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, ngmesh: netgen.libngpy._meshing.Mesh) -> None:
        """
        Make an NGSolve-mesh from a Netgen-mesh
        """
    @typing.overload
    def __init__(self, filename: str, comm: pyngcore.pyngcore.MPI_Comm = ...) -> None:
        """
        Load a mesh from file.
        In MPI-parallel mode the mesh is distributed over the MPI-group given by the communicator (WIP!)
        """
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def _updateBuffers(self) -> None:
        """
        Update NGSolve mesh information, needs to be called if Netgen mesh changes
        """
    def nnodes(self, arg0: ngsolve.fem.NODE_TYPE) -> int:
        """
        number of nodes given type
        """
    def nodes(self, node_type: ngsolve.fem.NODE_TYPE) -> MeshNodeRange:
        """
        iterable of mesh nodes of type node_type
        """
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm:
        """
        MPI-communicator the Mesh lives in
        """
    @property
    def deformation(self) -> ...:
        """
        mesh deformation
        """
    @deformation.setter
    def deformation(self, arg1: ...) -> None:
        ...
    @property
    def dim(self) -> int:
        """
        mesh dimension
        """
    @property
    def edges(self) -> MeshNodeRange:
        """
        iterable of mesh edges
        """
    @property
    def faces(self) -> MeshNodeRange:
        """
        iterable of mesh faces
        """
    @property
    def facets(self) -> MeshNodeRange:
        """
        iterable of mesh facets
        """
    @property
    def levels(self) -> int:
        """
        multigrid levels
        """
    @property
    def ne(self) -> int:
        """
        number of volume elements
        """
    @property
    def nedge(self) -> int:
        """
        number of edges
        """
    @property
    def nface(self) -> int:
        """
        number of faces
        """
    @property
    def nfacet(self) -> int:
        """
        number of facets
        """
    @property
    def ngmesh(self) -> netgen.libngpy._meshing.Mesh:
        """
        the Netgen mesh
        """
    @property
    def nv(self) -> int:
        """
        number of vertices
        """
    @property
    def vertices(self) -> MeshNodeRange:
        """
        iterable of mesh vertices
        """
class MeshNode(NodeId):
    """
    a node within a mesh
    """
    @property
    def edges(self) -> tuple:
        """
        tuple of global edge numbers
        """
    @property
    def elements(self) -> tuple:
        """
        tuple of global element-ids
        """
    @property
    def faces(self) -> tuple:
        """
        tuple of global face numbers
        """
    @property
    def point(self) -> tuple:
        """
        vertex coordinates
        """
    @property
    def vertices(self) -> tuple:
        """
        tuple of global vertex numbers
        """
class MeshNodeRange:
    def __getitem__(self, arg0: int) -> MeshNode:
        ...
    def __iter__(self) -> typing.Iterator[MeshNode]:
        ...
    def __len__(self) -> int:
        ...
class MultiGridPreconditioner(Preconditioner):
    """
    
     Keyword arguments can be:
    inverse: 
      Inverse type used in Preconditioner.
    test: bool = False
      Computes condition number for preconditioner, if testout file
      is set, prints eigenvalues to file.
    block: 
      use block-Jacobi/block-Gauss-Seidel
    blocktype: str = vertexpatch
      Blocktype used in compound FESpace for smoothing
      blocks. Options: vertexpatch, edgepatch
    updateall: bool = False
      Update all smoothing levels when calling Update
    smoother: string = 'point'
      Smoother between multigrid levels, available options are:
        'point': Gauss-Seidel-Smoother
        'line':  Anisotropic smoother
        'block': Block smoother
    coarsetype: string = direct
      How to solve coarse problem.
    coarsesmoothingsteps: int = 1
      If coarsetype is smoothing, then how many smoothingsteps will be done.
    updatealways: bool = False
    
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def SetDirectSolverCluster(self, arg0: list) -> None:
        ...
    def __init__(self, bf: BilinearForm, name: str = 'multigrid', lo_preconditioner: Preconditioner | None = None, **kwargs) -> None:
        ...
class NGS_Object:
    name: str
    @property
    def __memory__(self) -> list[tuple[str, int, int]]:
        ...
    @property
    def flags(self) -> pyngcore.pyngcore.Flags:
        ...
class Ngs_Element:
    def VB(self) -> VorB:
        """
        VorB of element
        """
    @property
    def edges(self) -> tuple:
        """
        tuple of global edge numbers
        """
    @property
    def elementnode(self) -> NodeId:
        """
        inner node, i.e. cell, face or edge node for 3D/2D/1D
        """
    @property
    def faces(self) -> tuple:
        """
        tuple of global face numbers
        """
    @property
    def facets(self) -> tuple:
        """
        tuple of global face, edge or vertex numbers
        """
    @property
    def index(self) -> int:
        """
        material or boundary condition index
        """
    @property
    def mat(self) -> str:
        """
        material or boundary condition label
        """
    @property
    def nr(self) -> int:
        """
        the element number
        """
    @property
    def type(self) -> ngsolve.fem.ET:
        """
        geometric shape of element
        """
    @property
    def valid(self) -> bool:
        """
        is element valid
        """
    @property
    def vertices(self) -> tuple:
        """
        tuple of global vertex numbers
        """
class NodalFESpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class NodeId:
    """
    an node identifier containing node type and node nr
    """
    def __eq__(self, arg0: NodeId) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, type: ngsolve.fem.NODE_TYPE, nr: int) -> None:
        ...
    def __ne__(self, arg0: NodeId) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @property
    def nr(self) -> int:
        """
        the node number
        """
    @property
    def type(self) -> ngsolve.fem.NODE_TYPE:
        """
        the node type
        """
class NodeRange:
    def __iter__(self) -> typing.Iterator[NodeId]:
        ...
    def __len__(self) -> int:
        ...
class NormalFacetFESpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    highest_order_dc: bool = False
      Splits highest order facet functions into two which are associated with
      the corresponding neighbors and are local dofs on the corresponding element
     (used to realize projected jumps)
    hide_highest_order_dc: bool = False
      if highest_order_dc is used this flag marks the corresponding local dofs
      as hidden dofs (reduces number of non-zero entries in a matrix). These dofs
      can also be compressed.
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class NormalFacetSurface(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class NumberSpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class ORDER_POLICY:
    """
    Enumeration of all supported order policies
    
    Members:
    
      CONSTANT
    
      NODETYPE
    
      VARIABLE
    
      OLDSTYLE
    """
    CONSTANT: typing.ClassVar[ORDER_POLICY]  # value = <ORDER_POLICY.CONSTANT: 0>
    NODETYPE: typing.ClassVar[ORDER_POLICY]  # value = <ORDER_POLICY.NODETYPE: 1>
    OLDSTYLE: typing.ClassVar[ORDER_POLICY]  # value = <ORDER_POLICY.OLDSTYLE: 3>
    VARIABLE: typing.ClassVar[ORDER_POLICY]  # value = <ORDER_POLICY.VARIABLE: 2>
    __members__: typing.ClassVar[dict[str, ORDER_POLICY]]  # value = {'CONSTANT': <ORDER_POLICY.CONSTANT: 0>, 'NODETYPE': <ORDER_POLICY.NODETYPE: 1>, 'VARIABLE': <ORDER_POLICY.VARIABLE: 2>, 'OLDSTYLE': <ORDER_POLICY.OLDSTYLE: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Periodic(FESpace):
    """
    Periodic or quasi-periodic Finite Element Spaces.
    The periodic fespace is a wrapper around a standard fespace with an 
    additional dof mapping for the periodic degrees of freedom. All dofs 
    on minion boundaries are mapped to their master dofs. Because of this, 
    the mesh needs to be periodic. Low order fespaces are currently not
    supported, so methods using them will not work.
    
    Parameters:
    
    fespace : ngsolve.comp.FESpace
        finite element space
    
    phase : list of Complex = None
        phase shift for quasi-periodic finite element space. The basis
        functions on the minion boundary are multiplied by the factor
        given in this list. If None (default) is given, a periodic
        fespace is created. The order of the list must match the order
        of the definition of the periodic boundaries in the mesh.
    
    used_idnrs : list of int = None
        identification numbers to be made periodic if you don't want to
        use all periodic identifications defined in the mesh, if None
        (default) all available periodic identifications are used.
    
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, fespace: FESpace, phase: list | None = None, use_idnrs: typing.Any = [], autoupdate: bool = False) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class PlateauFESpace(FESpace):
    """
    PlateauFESpace
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __init__(self, arg0: FESpace, arg1: list[Region]) -> None:
        ...
class Preconditioner(ngsolve.la.BaseMatrix, NGS_Object):
    """
    
     Keyword arguments can be:
    inverse: 
      Inverse type used in Preconditioner.
    test: bool = False
      Computes condition number for preconditioner, if testout file
      is set, prints eigenvalues to file.
    block: 
      use block-Jacobi/block-Gauss-Seidel
    blocktype: 
      blocktype like 'vertexpatch', 'edgepatch', ...
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def Test(self) -> None:
        ...
    def Update(self) -> None:
        """
        Update preconditioner
        """
    def __init__(self, bf: BilinearForm, type: str, **kwargs) -> None:
        ...
    @property
    def mat(self) -> BaseMatrix:
        """
        matrix of the preconditioner
        """
class ProductSpace(FESpace):
    """
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def Embedding(self, component: int) -> BaseMatrix:
        """
        create embedding operator for this component
        """
    def Range(self, component: int) -> ngsolve.la.DofRange:
        """
                 Return interval of dofs of a component of a product space.
        
        Parameters:
        
        component : int
          input component
        """
    def Restriction(self, component: int) -> BaseMatrix:
        """
        create restriction operator onto this component
        """
    def SetDoSubspaceUpdate(self, arg0: bool) -> None:
        ...
    def VSEmbedding(self, VOL_or_BND: VorB = ...) -> ngsolve.bla.MatrixD | None:
        """
        get the vector space embedding (returns None if the embedding is 'identity')
        """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, *args) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def components(self) -> Array[FESpace]:
        """
        Return a list of the components of a product space
        """
    @property
    def embeddings(self) -> list:
        """
        returns a list of embeddings for the component spaces
        """
    @property
    def restrictions(self) -> list:
        """
        returns a list of restrictions onto the component spaces
        """
class Prolongation:
    def CreateMatrix(self, finelevel: int) -> ngsolve.la.SparseMatrixd:
        ...
    def LevelDofs(self, level: int) -> ngsolve.la.DofRange:
        ...
    def Operator(self, finelevel: int) -> BaseMatrix:
        ...
    def Prolongate(self, finelevel: int, vec: ngsolve.la.BaseVector) -> None:
        ...
    def Restrict(self, finelevel: int, vec: ngsolve.la.BaseVector) -> None:
        ...
class ProxyFunction(ngsolve.fem.CoefficientFunction):
    """
    
    Either FESpace.TrialFunction or FESpace.TestFunction. Is a
    placeholder coefficient function for Symbolic Integrators. The
    integrators will replace it with the basis functions of the finite element space
    when building the system matrices.
    
    """
    def Deriv(self) -> ProxyFunction:
        """
        take canonical derivative (grad, curl, div)
        """
    def Operator(self, name: str) -> ProxyFunction:
        """
        Use an additional operator of the finite element space
        """
    def Operators(self) -> list:
        """
        returns list of available differential operators
        """
    def Other(self, bnd: typing.Any = ...) -> ProxyFunction:
        """
        take value from neighbour element (DG)
        """
    def ReplaceFunction(self, arg0: ...) -> ...:
        """
        replace proxyfunction by GridFunction, apply the same operator
        """
    def Trace(self) -> ProxyFunction:
        """
        take canonical boundary trace
        """
    def VSEmbedding(self) -> ngsolve.bla.MatrixD | None:
        """
        get the vector space embedding (returns None if the embedding is 'identity')
        """
    def __diffop__(self) -> ngsolve.fem.DifferentialOperator:
        ...
    def __init__(self, arg0: ProxyFunction) -> None:
        ...
    @property
    def anti_dt(self) -> ProxyFunction:
        """
        time anti-derivative
        """
    @property
    def derivname(self) -> str:
        """
        name of the canonical derivative
        """
    @property
    def dt(self) -> ProxyFunction:
        """
        time derivative
        """
    @property
    def dt_order(self) -> int:
        """
        time anti-derivative
        """
    @property
    def primary(self) -> ngsolve.fem.CoefficientFunction:
        """
        returns my primary proxy
        """
    @property
    def space(self) -> ...:
        """
        the finite element space
        """
class QuasiPeriodicC(Periodic):
    """
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class QuasiPeriodicD(Periodic):
    """
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class Region:
    """
    a subset of volume or boundary elements
    """
    def Boundaries(self) -> Region:
        ...
    def Elements(self) -> typing.Iterator[Ngs_Element]:
        ...
    def Mask(self) -> pyngcore.pyngcore.BitArray:
        """
        BitArray mask of the region
        """
    def Neighbours(self, arg0: VorB) -> Region:
        ...
    def Split(self) -> list:
        """
        Split region in domains/surfaces/...
        """
    def VB(self) -> VorB:
        """
        VorB of the region
        """
    @typing.overload
    def __add__(self, arg0: Region) -> Region:
        ...
    @typing.overload
    def __add__(self, arg0: str) -> Region:
        ...
    def __call__(self, arg0: numpy.ndarray[numpy.float64], arg1: numpy.ndarray[numpy.float64], arg2: numpy.ndarray[numpy.float64]) -> typing.Any:
        ...
    def __eq__(self, arg0: Region) -> bool:
        ...
    def __getstate__(self) -> tuple:
        ...
    def __hash__(self) -> int:
        ...
    @typing.overload
    def __init__(self, mesh: ..., vb: VorB, name: str) -> None:
        ...
    @typing.overload
    def __init__(self, mesh: ..., vb: VorB, mask: pyngcore.pyngcore.BitArray) -> None:
        ...
    def __invert__(self) -> Region:
        ...
    @typing.overload
    def __mul__(self, arg0: Region) -> Region:
        ...
    @typing.overload
    def __mul__(self, arg0: str) -> Region:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @typing.overload
    def __sub__(self, arg0: Region) -> Region:
        ...
    @typing.overload
    def __sub__(self, arg0: str) -> Region:
        ...
    @property
    def mesh(self) -> ...:
        ...
class Reorder(FESpace):
    """
    Reordered Finite Element Spaces.
    ...
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def GetClusters(self) -> pyngcore.pyngcore.Table_I:
        ...
    def __init__(self, fespace: FESpace, autoupdate: bool = False) -> None:
        ...
class SumOfIntegrals:
    def Compile(self, realcompile: bool = False, wait: bool = False, keep_files: bool = False) -> SumOfIntegrals:
        ...
    def Derive(self, arg0: ngsolve.fem.CoefficientFunction, arg1: ngsolve.fem.CoefficientFunction) -> SumOfIntegrals:
        """
        depricated: use 'Diff' instead
        """
    def Diff(self, arg0: ngsolve.fem.CoefficientFunction, arg1: ngsolve.fem.CoefficientFunction) -> SumOfIntegrals:
        ...
    def DiffShape(self, arg0: ngsolve.fem.CoefficientFunction) -> SumOfIntegrals:
        ...
    def GetProxies(self, trial: bool = True) -> Array[ProxyFunction]:
        ...
    def Replace(self, arg0: dict[ngsolve.fem.CoefficientFunction, ngsolve.fem.CoefficientFunction]) -> SumOfIntegrals:
        ...
    def SetDefinedOnElements(self, arg0: pyngcore.pyngcore.BitArray) -> None:
        ...
    def __add__(self, arg0: SumOfIntegrals) -> SumOfIntegrals:
        ...
    def __getitem__(self, arg0: int) -> Integral:
        ...
    def __len__(self) -> int:
        ...
    def __radd__(self, arg0: int) -> SumOfIntegrals:
        ...
    @typing.overload
    def __rmul__(self, arg0: float) -> SumOfIntegrals:
        ...
    @typing.overload
    def __rmul__(self, arg0: complex) -> SumOfIntegrals:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: SumOfIntegrals) -> SumOfIntegrals:
        ...
    @property
    def linearization(self) -> None:
        ...
    @linearization.setter
    def linearization(self, arg1: SumOfIntegrals) -> None:
        ...
class SurfaceL2(FESpace):
    """
    An L2-conforming finite element space.
    
    The L2 finite element space on surfaces consists of element-wise polynomials,
    which are discontinuous from element to element. It uses an
    L2-orthogonal hierarchical basis which leads to orthogonal
    mass-matrices on non-curved elements.
    
    The L2 space supports element-wise variable order, which can be set
    for ELEMENT-nodes.
    
    Per default, all dofs are local dofs and are condensed if static
    condensation is performed. The lowest order can be kept in the
    WIRE_BASKET via the flag 'lowest_order_wb=True'.
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    lowest_order_wb: bool = False
      Keep lowest order dof in WIRE_BASKET and make other dofs LOCAL
    discontinuous: bool = False
      Make all dofs LOCAL
    dual_mapping: bool = False
      element mapping includes inverse measure
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class SymbolTable_D:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> float:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_D:
    def GetName(self, pos: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> float:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_N5ngfem19CoefficientFunctionE:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> ngsolve.fem.CoefficientFunction:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> ngsolve.fem.CoefficientFunction:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_N6ngcomp10LinearFormE:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> LinearForm:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> LinearForm:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_N6ngcomp12BilinearFormE:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> BilinearForm:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> BilinearForm:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_N6ngcomp12GridFunctionE:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> GridFunction:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> GridFunction:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_N6ngcomp14PreconditionerE:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> Preconditioner:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> Preconditioner:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class SymbolTable_sp_N6ngcomp7FESpaceE:
    def GetName(self, arg0: int) -> str:
        ...
    def __contains__(self, arg0: str) -> bool:
        ...
    @typing.overload
    def __getitem__(self, name: str) -> FESpace:
        ...
    @typing.overload
    def __getitem__(self, pos: int) -> FESpace:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
class TangentialFacetFESpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    highest_order_dc: bool = False
      Splits highest order facet functions into two which are associated with
      the corresponding neighbors and are local dofs on the corresponding element
     (used to realize projected jumps)
    hide_highest_order_dc: bool = False
      if highest_order_dc is used this flag marks the corresponding local dofs
      as hidden dofs (reduces number of non-zero entries in a matrix). These dofs
      can also be compressed.
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class TangentialSurfaceL2(FESpace):
    """
    An tangential, L2-conforming finite element space.
    
     (tbd)
    The L2 finite element space on surfaces consists of element-wise polynomials,
    which are discontinuous from element to element. It uses an
    L2-orthogonal hierarchical basis which leads to orthogonal
    mass-matrices on non-curved elements.
    
    The L2 space supports element-wise variable order, which can be set
    for ELEMENT-nodes.
    
    Per default, all dofs are local dofs and are condensed if static
    condensation is performed. The lowest order can be kept in the
    WIRE_BASKET via the flag 'lowest_order_wb=True'.
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    piola: bool = False
      Use Piola-mapping
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VTKOutput:
    @typing.overload
    def Do(self, time: float = -1, vb: VorB = ...) -> str:
        """
        Write mesh and fields to file. When called several times on the same object
        an index is added to the output file name. A meta file (.pvd) is written 
        (unless in legacy mode).
        
        Returns string of the output filename.
        
        Parameters:
        
        time : 
          associate a time to the current output
        
        vb: VOL_or_BND (default VOL)
          defines if output is done on the volume (VOL) or surface mesh (BND).
                    .
        """
    @typing.overload
    def Do(self, time: float = -1, vb: VorB = ..., drawelems: pyngcore.pyngcore.BitArray) -> str:
        """
        Write mesh and fields to file. When called several times on the same object
        an index is added to the output file name. A meta file (.pvd) is written 
        (unless in legacy mode).
        
        Returns string of the output filename.
        
        Parameters:
        
        time : 
          associate a time to the current output (default: output counter)
        
        vb: VOL_or_BND (default VOL)
          defines if output is done on the volume (VOL) or surface mesh (BND).
        
        drawelems: BitArray
          defines the submesh (set of elements) that are (only) used for drawing. 
                    .
        """
    def __init__(self, ma: Mesh, coefs: list = [], names: list = [], filename: str = 'vtkout', subdivision: int = 0, only_element: int = -1, floatsize: str = 'double', legacy: bool = False, order: int = 1) -> None:
        """
        VTK output class. Allows to put mesh and field information of several CoefficientFunctions into a VTK file.
        (Can be used by independent visualization software, e.g. ParaView).
        
        When run in parallel, rank 0 stores no vtk output, but writes the pvd-file that links all parallel
        output together.
        
        Parameters:
        
        ma : ngsolve mesh
          mesh (Note: if a deformation is set, the output will be w.r.t. the deformed state of the mesh)
        
        coefs: list of CoefficientFunctions
          list of CFs that are stored as fields in the Paraview output
        
        names : list of strings
          labels for the fields that are put in the output file
        
        filename : string (default: \\"output\\")
          name of the output file ( .vtu file ending is added or .vtk file ending is added (legacy mode) ).
          If run in parallel, the suffix \\"_procxyz\\" is added (xyz a number). 
          If output is written several times, the ending \\"_stepxyz\\" is added (xyz a counter). 
          If run in parallel or the output is called several times a meta file with ending .pvd is also generated for convenience.
        
        subdivision : int
          Number of subdivision (bisections in each direction) that are applied
          (Note that only vertex values are stored otherwise rendering the output information piecewise linear only)
        
        only_element : int
          only work on one specific element (default: -1 which means `draw all elements`)
        
        floatsize : string in {\\"single\\", \\"double\\" }   object
          defines the precision of the output data (default is \\"double\\", \\"single\\" can be used to reduce output)
        
        legacy : bool (default: False)
          defines if legacy-VTK output shall be used 
        
        order : int (default: 1)
          allowed values: 1,2
                    .
        """
class Variation:
    def Compile(self, realcompile: bool = False, wait: bool = False, keep_files: bool = False) -> Variation:
        ...
    def __init__(self, arg0: SumOfIntegrals) -> None:
        ...
class VectorFacetFESpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VectorFacetSurface(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VectorH1(ProductSpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    interleaved: bool = False
      ordering of dofs changed to x0, y0, z0, x1 ....
    dirichletx: regexpr
      Regular expression string defining the dirichlet boundary
      on the first component of VectorH1.
      More than one boundary can be combined by the | operator,
      i.e.: dirichletx = 'top|right'
    dirichlety: regexpr
      Dirichlet boundary for the second component
    dirichletz: regexpr
      Dirichlet boundary for the third component
    dirichletx_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D, on the first component.
      More than one bboundary can be combined by the | operator,
      i.e.: dirichletx_bbnd = 'top|right'
    dirichlety_bbnd: regexpr
      Dirichlet bboundary for the second component
    dirichletz_bbnd: regexpr
      Dirichlet bboundary for the third component
    dirichletx_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D, on the first component.
      More than one bbboundary can be combined by the | operator,
      i.e.: dirichletx_bbbnd = 'top|right'
    dirichlety_bbbnd: regexpr
      Dirichlet bbboundary for the second component
    dirichletz_bbbnd: regexpr
      Dirichlet bbboundary for the third component
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VectorL2(ProductSpace):
    """
    A vector-valued L2-conforming finite element space.
    
    The Vector-L2 finite element space is a product-space of L2 spaces,
    where the number of components coincides with the mesh dimension.
    
    It is implemented by means of a CompoundFESpace, as one could do it at the
    user-level. Additionally, some operators are added for convenience and performance:
    One can evaluate the vector-valued function, and one can take the gradient.
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    piola: bool = False
      Use Piola transform to map to physical element
      allows to use the div-differential operator.
    covariant: bool = False
      Use the covariant transform to map to physical element
      allows to use the curl-differential operator.
    all_dofs_together: bool = True
      dofs within one scalar component are together.
    hide_all_dofs: bool = False
      all dofs are condensed without a global dofnr
    lowest_order_wb: bool = False
      Keep lowest order dof in WIRE_BASKET
    tp: bool = False
      Use sum-factorization for evaluation
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VectorNodalFESpace(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VectorSurfaceL2(FESpace):
    """
    
    
    
    Keyword arguments can be:
    
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    @staticmethod
    def __flags_doc__() -> dict:
        ...
    def __getstate__(self: FESpace) -> tuple:
        ...
    def __init__(self, mesh: Mesh, **kwargs) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VectorValued(ProductSpace):
    """
    
     Keyword arguments can be:
    order: int = 1
      order of finite element space
    complex: bool = False
      Set if FESpace should be complex
    dirichlet: regexpr
      Regular expression string defining the dirichlet boundary.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet = 'top|right'
    dirichlet_bbnd: regexpr
      Regular expression string defining the dirichlet bboundary,
      i.e. points in 2D and edges in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbnd = 'top|right'
    dirichlet_bbbnd: regexpr
      Regular expression string defining the dirichlet bbboundary,
      i.e. points in 3D.
      More than one boundary can be combined by the | operator,
      i.e.: dirichlet_bbbnd = 'top|right'
    definedon: Region or regexpr
      FESpace is only defined on specific Region, created with mesh.Materials('regexpr')
      or mesh.Boundaries('regexpr'). If given a regexpr, the region is assumed to be
      mesh.Materials('regexpr').
    dim: int = 1
      Create multi dimensional FESpace (i.e. [H1]^3)
    dgjumps: bool = False
      Enable discontinuous space for DG methods, this flag is needed for DG methods,
      since the dofs have a different coupling then and this changes the sparsity
      pattern of matrices.
    autoupdate: bool = False
      Automatically update on a change to the mesh.
    low_order_space: bool = True
      Generate a lowest order space together with the high-order space,
      needed for some preconditioners.
    hoprolongation: bool = False
      Create high order prolongation operators,
      only available for H1 and L2 on simplicial meshes
    order_policy: ORDER_POLICY = ORDER_POLICY.OLDSTYLE
      CONSTANT .. use the same fixed order for all elements,
      NODAL ..... use the same order for nodes of same shape,
      VARIABLE ... use an individual order for each edge, face and cell,
      OLDSTYLE .. as it used to be for the last decade
    print: bool = False
      (historic) print some output into file set by 'SetTestoutFile'
    """
    def __getstate__(self) -> tuple:
        ...
    def __init__(self, space: FESpace, dim: int | None = None, interleaved: bool = False, autoupdate: bool = False) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class VorB:
    """
    Enum specifying the codimension. VOL is volume, BND is boundary and BBND is codimension 2 (edges in 3D, points in 2D)
    
    Members:
    
      VOL
    
      BND
    
      BBND
    
      BBBND
    """
    BBBND: typing.ClassVar[VorB]  # value = <VorB.BBBND: 3>
    BBND: typing.ClassVar[VorB]  # value = <VorB.BBND: 2>
    BND: typing.ClassVar[VorB]  # value = <VorB.BND: 1>
    VOL: typing.ClassVar[VorB]  # value = <VorB.VOL: 0>
    __members__: typing.ClassVar[dict[str, VorB]]  # value = {'VOL': <VorB.VOL: 0>, 'BND': <VorB.BND: 1>, 'BBND': <VorB.BBND: 2>, 'BBBND': <VorB.BBBND: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def BndElementId(nr: int) -> ElementId:
    """
    Creates an element-id for a boundary element
    
    Parameters:
    
    nr : int
      input Bnd element number
    """
def BoundaryFromVolumeCF(vol_cf: ngsolve.fem.CoefficientFunction) -> ngsolve.fem.CoefficientFunction:
    """
    Allows the evaluation of volumetric functions on the boundary.
    
    When evaluated on a boundary element, this function searches for the associated
    volume element, transforms the local coordinates, and evaluates the function in the
    volume. A typical use case is to visualize L2-functions, or mechanical stresses at
    the boundary.
    
    It is different from the boundary Trace()-operator. The trace provides a function
    which is defined by boundary degrees of freedom only. E.g. the trace of an H(div)
    function is only the normal component, while the BoundaryFromVolumeCF gives the
    whole function. Obviously, the Trace() function is cheaper to evaluate.
    
    If called on an interface, it evaluates from one side (which one is not specified).
    If the function is only defined on one side, this side will be taken. One can use
    a domain-wise CF to define a function only locally:
    uloc = CoefficientFunction( [None, None, u, None] )
    """
def CompressCompound(fespace: FESpace, active_dofs: typing.Any = ...) -> FESpace:
    ...
def ConvertOperator(spacea: FESpace, spaceb: FESpace, trial_proxy: ProxyFunction = None, trial_cf: ngsolve.fem.CoefficientFunction = None, definedon: Region | None = None, vb: VorB = ..., range_dofs: pyngcore.pyngcore.BitArray = None, localop: bool = False, parmat: bool = True, use_simd: bool = True, bonus_intorder_ab: int = 0, bonus_intorder_bb: int = 0, geom_free: bool = False) -> BaseMatrix:
    """
    A conversion operator between FESpaces. Embedding if spacea is a subspace of spaceb, otherwise an interpolation operator defined by element-wise application of dual shapes (and averaging between elements).
    
    Parameters:
    
    spacea: ngsolve.comp.FESpace
      the origin space
    
    spaceb: ngsolve.comp.FESpace
      the goal space
    
    trial_proxy: ngsolve.comp.ProxyFunction
      (optional) Must be a trial-proxy on spacea. If given, instead of a FE-function funca from spacea, the operator converts trial_proxy(funca) to spaceb.
    
    trial_proxy: ngsolve.comp.CoefficientFunction
      (optional) Same as trial_proxy, but takes any CoefficientFunction. Use at your own peril.
    
    definedon: object
      what part of the domain to restrict the operator to
    
    vb: ngsolve.comp.VorB
      what kind of co-dimension elements to convert on VOL, BND, BBND, ...
    
    range_dofs: ngsolve.ngstd.BitArray
      Projects out DOFs in the range where range_dofs are not set
    
    localop: bool
      True -> do not average across MPI boundaries. No effect for non MPI-paralell space. Use carefully!!
    
    parmat: bool
      If True, returns a ParallelMatrix for MPI-parallel spaces. If False, or for non MPI-parallel spaces, returns a local BaseMatrix.
    
    use_simd:
      False -> Do not use SIMD for setting up the Matrix. (for debugging purposes).
    
    bonus_intorder_ab/bb: int
      Bonus integration order for spacea/spaceb and spaceb/spaceb integrals. Can be useful for curved elements. Should only be necessary for
    spacea/spaceb integrals.
    
    geom_free:
      If True, assembles a matrix-free operator.
    """
def FromArchiveCF(arg0: str, arg1: bool) -> ngsolve.fem.CoefficientFunction:
    ...
def FromArchiveFESpace(arg0: str, arg1: bool) -> FESpace:
    ...
def FromArchiveMesh(arg0: str, arg1: bool) -> netgen.libngpy._meshing.Mesh:
    ...
@typing.overload
def Integrate(cf: ngsolve.fem.CoefficientFunction, mesh: Mesh | Region, VOL_or_BND: VorB = ..., order: int = 5, definedon: Region = None, region_wise: bool = False, element_wise: bool = False) -> typing.Any:
    """
    Parameters
    ----------
    
    cf: ngsolve.CoefficientFunction
      Function to be integrated. Can be vector valued, then the result is an array. If you want to integrate
      a lot of functions on the same domain, it will be faster to put them into a vector valued function,
      NGSolve will then be able to use parallelization and SIMD vectorization more efficiently.
    
    mesh: ngsolve.Mesh
      The mesh to be integrated on.
    
    VOL_or_BND: ngsolve.VorB = VOL
      Co-dimension to be integrated on. Historically this could be volume (VOL) or boundary (BND). If your mesh
      contains co-dim 2 elements this can now be BBND (edges in 3d) as well.
    
    order: int = 5
      Integration order, polynomials up to this order will be integrated exactly.
    
    definedon: ngsolve.Region
      Region to be integrated on. Such region can be created with mesh.Boundaries('bcname') or mesh.Materials('matname')
      it will overwrite the VOL_or_BND argument if given.
    
    region_wise: bool = False
      Integrates region wise on the co-dimension given by VOL_or_BND. Returns results as an array, matching the array
      returned by mesh.GetMaterials() or mesh.GetBoundaries(). Does not support vector valued CoefficientFunctions.
    
    element_wise: bool = False
      Integrates element wise and returns result in a list. This is typically used for local error estimators.
      Does not support vector valued CoefficientFunctions
    """
@typing.overload
def Integrate(igls: SumOfIntegrals, mesh: Mesh, element_wise: bool = False) -> typing.Any:
    ...
def Interpolate(cf: ngsolve.fem.CoefficientFunction, space: FESpace, bonus_intorder: int = 0, operator: str | None = None) -> ngsolve.fem.CoefficientFunction:
    """
    Interpolate a CoefficientFunction into the finite element space.
    The interpolation is canonical interpolation using dual shapes.
    The result is a CoefficientFunction.
    Interpolation is done on the fly for each element, no global GridFunction is allocated.
    """
def KSpaceCoeffs(arg0: GridFunction, arg1: GridFunction, arg2: float, arg3: float) -> None:
    ...
def MatrixFreeOperator(arg0: FESpace, arg1: typing.Any) -> BaseMatrix:
    ...
def PatchwiseSolve(bf: SumOfIntegrals, lf: SumOfIntegrals, gf: GridFunction) -> None:
    ...
def Prolongate(arg0: GridFunction, arg1: GridFunction) -> None:
    ...
def ProlongateCoefficientFunction(arg0: ngsolve.fem.CoefficientFunction, arg1: int, arg2: FESpace) -> ngsolve.fem.CoefficientFunction:
    ...
def RegisterPreconditioner(name: str, makepre: typing.Any, docflags: dict = {}) -> None:
    """
    register creator-function makepre(BaseMatrix,FreeDofs)->BaseMatrix
    """
def SetHeapSize(size: int) -> None:
    """
    Set a new heapsize.
    
    Parameters:
    
    size : int
      input heap size
    """
def SetTestoutFile(file: str) -> None:
    """
    Enable some logging into file with given filename
    
    Parameters:
    
    file : string
      input file name
    """
def SymbolicBFI(form: ngsolve.fem.CoefficientFunction, VOL_or_BND: VorB = ..., element_boundary: bool = False, skeleton: bool = False, definedon: Region | list | None = None, intrule: ngsolve.fem.IntegrationRule = ..., bonus_intorder: int = 0, definedonelements: pyngcore.pyngcore.BitArray = None, simd_evaluate: bool = True, element_vb: VorB = ..., geom_free: bool = False, deformation: GridFunction = None) -> ngsolve.fem.BFI:
    """
    A symbolic bilinear form integrator, where test and trial functions, CoefficientFunctions, etc. can be used to formulate PDEs in a symbolic way.
    
    Parameters:
    
    form : ngsolve.fem.CoefficientFunction
      input the symbolic right hand side form
    
    VOL_or_BND : ngsolve.comp.VorB
      input VOL, BND, BBND, ...
    
    element_boundary : bool
      input element_boundary. True -> iterates over all element boundaries, but uses volume transformations
    
    skeleton : bool
      input skeleton. True -> iterates over all faces, but uses volume transformations
    
    definedon : object
      input definedon region
    
    intrule : ngsolve.fem.IntegrationRule
      input integration rule
    
    bonus_intorder : int
      input additional integration order
    
    definedonelements : object
      input definedonelements
    
    simd_evaluate : bool
      input simd_evaluate. True -> tries to use SIMD for faster evaluation
    
    element_vb : ngsolve.comp.VorB
      input element_vb. Used for skeleton formulation. VOL -> interior faces, BND -> boundary faces
    
    deformation : ngsolve.comp.GridFunction
      input GridFunction to transform/deform the bilinear form with
    """
def SymbolicEnergy(form: ngsolve.fem.CoefficientFunction, VOL_or_BND: VorB = ..., definedon: typing.Any = ..., element_boundary: bool = False, bonus_intorder: int = 0, definedonelements: typing.Any = ..., simd_evaluate: bool = True, element_vb: VorB = ..., deformation: GridFunction = None) -> ngsolve.fem.BFI:
    """
    A symbolic energy form integrator, where test and trial functions, CoefficientFunctions, etc. can be used to formulate PDEs in a symbolic way.
    
    Parameters:
    
    form : ngsolve.fem.CoefficientFunction
      input the symbolic right hand side form
    
    VOL_or_BND : ngsolve.comp.VorB
      input VOL, BND, BBND, ...
    
    definedon : object
      input definedon region
    
    element_boundary : bool
      input element_boundary. True -> iterates over all element boundaries, but uses volume transformations
    
    bonus_intorder : int
      input additional integration order
    
    definedonelements : object
      input definedonelements
    
    simd_evaluate : bool
      input simd_evaluate. True -> tries to use SIMD for faster evaluation
    
    element_vb : ngsolve.fem.VorB
      input eleemnt VorB
    
    deformation : ngsolve.comp.GridFunction
      input GridFunction to transform/deform the bilinear form with
    """
def SymbolicLFI(form: ngsolve.fem.CoefficientFunction, VOL_or_BND: VorB = ..., element_boundary: bool = False, skeleton: bool = False, definedon: Region | list | None = None, intrule: ngsolve.fem.IntegrationRule = ..., bonus_intorder: int = 0, definedonelements: pyngcore.pyngcore.BitArray = None, simd_evaluate: bool = True, element_vb: VorB = ..., deformation: GridFunction = None) -> ngsolve.fem.LFI:
    """
    A symbolic linear form integrator, where test and trial functions, CoefficientFunctions, etc. can be used to formulate right hand sides in a symbolic way.
    
    Parameters:
    
    form : ngsolve.fem.CoefficientFunction
      input the symbolic right hand side form
    
    VOL_or_BND : ngsolve.comp.VorB
      input VOL, BND, BBND, ...
    
    element_boundary : bool
      input element_boundary. True -> iterates over all element boundaries, but uses volume transformations
    
    skeleton : bool
      input skeleton. True -> iterates over all faces, but uses volume transformations
    
    definedon : object
      input definedon region
    
    intrule : ngsolve.fem.IntegrationRule
      input integration rule
    
    bonus_intorder : int
      input additional integration order
    
    definedonelements : object
      input BitArray that marks all elements or facets (for skeleton-integrators) that the integrator is applied on
    
    simd_evaluate : bool
      input simd_evaluate. True -> tries to use SIMD for faster evaluation
    
    element_vb : ngsolve.fem.VorB
      input element VorB
    
    deformation : ngsolve.comp.GridFunction
      input GridFunction to transform/deform the linear form with
    """
def SymbolicTPBFI(form: ngsolve.fem.CoefficientFunction, VOL_or_BND: VorB = ..., element_boundary: bool = False, skeleton: bool = False, definedon: typing.Any = ...) -> ngsolve.fem.BFI:
    ...
def TensorProductFESpace(spaces: list, flags: pyngcore.pyngcore.Flags = ...) -> FESpace:
    ...
@typing.overload
def TensorProductIntegrate(arg0: GridFunction, arg1: list, arg2: ngsolve.fem.CoefficientFunction) -> float:
    ...
@typing.overload
def TensorProductIntegrate(gftp: GridFunction, gfx: GridFunction, weight: ngsolve.fem.CoefficientFunction = None) -> None:
    ...
@typing.overload
def ToArchive(arg0: netgen.libngpy._meshing.Mesh, arg1: bool) -> bytes:
    ...
@typing.overload
def ToArchive(arg0: ngsolve.fem.CoefficientFunction, arg1: bool) -> bytes:
    ...
@typing.overload
def ToArchive(arg0: FESpace, arg1: bool) -> bytes:
    ...
@typing.overload
def ToArchive(arg0: Mesh, arg1: ngsolve.fem.CoefficientFunction, arg2: bool) -> bytes:
    ...
@typing.overload
def Transfer2StdMesh(gftp: GridFunction, gfstd: GridFunction) -> None:
    ...
@typing.overload
def Transfer2StdMesh(arg0: ngsolve.fem.CoefficientFunction, arg1: GridFunction) -> None:
    ...
BBBND: VorB  # value = <VorB.BBBND: 3>
BBND: VorB  # value = <VorB.BBND: 2>
BND: VorB  # value = <VorB.BND: 1>
VOL: VorB  # value = <VorB.VOL: 0>
ngsglobals: GlobalVariables  # value = <ngsolve.comp.GlobalVariables object>
