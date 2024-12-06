import numpy as np
import numpy.typing as npt
import sympy
from scipy.interpolate import InterpolatedUnivariateSpline as IUS
from sympy import Add

# the only sympy symbol we use is 'x_sym'
x_sym = sympy.symbols("x_sym")


def compute_values(
    collocation_points: dict,
    x: npt.NDArray,
    y: npt.NDArray,
) -> dict:
    """
     Given a dictionary of collocation points compute the collocation values. x and y are training
     data on a fine grid which are interpolated so that derivatives can be estimated.

     Parameters
     ----------
     collocation_points : dict
         Collocation points supplied as a dictionary with integer keys representing the order of
         derivative and the values are a list of numbers that are the values of the x-coordinate to
         evaluate the (x,y) data at e.g. {0:[], 1:[], ...}.
     x : npt.NDArray
         Independent variable
    y : npt.NDArray
         Dependent variable

     Returns
     -------
     cv : dict
         A dictionary of collocation values (cv). The dictionary has the same
         format as the input collocation_points dict.
    """
    cp = collocation_points.copy()
    iy = IUS(x, y)
    cv = {d: np.asarray([iy.derivative(d)(v) for v in cp[d]]) for d in cp.keys()}
    return cv


class CollocationModel:
    """
    CollocationModel is a class that can fit a linear model to data
    using the collocation point method. The collocation points are
    not restricted to being just the value of the function at the collocation
    points but you can also specify the value to be higher derivatives
    of the model at the collocation points.

    For more details on this implementation see Section 5 in:
    [PhysRevD.109.104045](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.109.104045).
    """

    def __init__(
        self,
        collocation_points: dict,
        collocation_values: dict,
        ansatz: Add,
        sub_dict: dict | None = None,
    ):
        """
        collocation_points : dict
            dictionary with integer keys representing the order
            of derivative and the values are a list of numbers that are the
            values of the x-coordinate to evaluate the rhs at.
            {0:[], 1:[], ...}
            [[d0], [d1], [d2], ...]
            d0 == points to evaluate RHS at zeroth derivative
            d1 == points to evaluate RHS at 1st derivative
            d2 == points to evaluate RHS at 2nd derivative ...etc
            The sum total of elments of the flattened list is the
            number of equations and equivalently the number of
            coefficients to fix by comparing with data.
            Data is provided as the right hand side (RHS).
        collocation_values : dict
            the collocation values are also called the right hand side (rhs)
            provided in the same format as collocation_points
        ansatz:
            sympy stuff
            this must be a linear-in-coefficients ansatz so that
            it can be expressed in a matrix form.
            Ansatz is just another word for functional form / model.
            For example a linear model/ansatz could be y(x) = a*x + b
        sub_dict:
            this is a dictionary mapping sympy symbol name to a constant
            this is needed because after we (potentially) differentiate the ansatz
            term we need to evaluate the expression so we need a value for these constants
            Note: currently we only support additionaly constants that linearly multiply the
            variables.
            e.g. if the ansatz is 1 + x then you could use sub_dict for ansatz of the form
            1 + x * omega but not for something like 1 + x + omega.
        """
        self.collocation_points = collocation_points
        # self.collocation_values = collocation_values
        self.rhs = collocation_values
        self.ansatz = ansatz.copy()
        self.sub_dict = sub_dict

        self.setup()

    def setup(self):
        # flatten collocation points
        self.collocation_points_1d = np.concatenate(
            [v for _, v in self.collocation_points.items()]
        )
        # set degrees of freedom / number of free parameters expected
        self.dof = len(self.collocation_points_1d)
        # create some human readable names for the collocation points
        # for example if collocation_points = {0:[1,2,3], 1:[2,3]}
        # then tags = ["d0_c1","d0_c2","d0_c3", "d1_c1", "d1_c2"]
        self.tags = []
        for d in self.collocation_points.keys():
            for c in range(len(self.collocation_points[d])):
                self.tags.append(f"d{d}_c{c}")

        self.lambdify_ansatz(sympy_args=(x_sym))

        # flatten right hand side
        self.rhs_1d = np.concatenate([v for _, v in self.rhs.items()])
        assert len(self.collocation_points_1d) == len(
            self.rhs_1d
        ), "number of collocation points and rhs are not the same"

        msg = f"""ansatz doesn't contain correct number of degrees of freedom.
 dof = {self.dof}. Ansatz has {len(self.ansatz.args)}"""
        assert self.dof == len(self.ansatz.args), msg

        self.create_information_matrix()
        self.solve()

    def lambdify_ansatz(self, sympy_args):
        """
        Create a sympy lambda function for each of the terms in the ansatz.
        sympy_args: these are the sympy symbols that that lambda function will
            be a function of
        """
        # terms_fn: list of sympy.lambdify functions
        # each element of the list corresponds to each term in the ansatz
        ansatz = self.ansatz.copy()
        if self.sub_dict is not None:
            ansatz = ansatz.subs(self.sub_dict)
        # self.terms_fn = [sympy.lambdify(sympy_args, term, "numpy") for term in self.ansatz.args]
        self.terms_fn = [sympy.lambdify(sympy_args, term, "numpy") for term in ansatz.args]

    def create_information_matrix(self):
        """
        Evaluate the ansatz at the collocation_points and create the information matrix. It's
        elements are the values of the variables (also called indeterminates) of the Ansatz
        evaluated at each of the collocation points.

        The information matrix is calculated using two for loops. The first loop is over
        the derivative order and the second loop is over collation points.
        Each iteration of this double for loop creates a row in the information matrix.
        For example if collocation_points = {0:[0,1], 1:[0]}
        then the rows in information_matrix matrix will correspond to
        [
            [derivative=0, collocation_point=0],
            [derivative=0, collocation_point=1],
            [derivative=1, collocation_point=0]
        ]

        extra_sub_dict: this is a dictionary mapping sympy symbol name to a constant
            this is needed because after we (potentially) differentiate the ansatz
            term we need to evaluate the expression so we need a value for these constants
        """
        # compute information matrix

        # need to compute derivatives term by term
        # that way we can be sure that we arrive at the correct number of
        # elements in each row
        # and then we can correctly handle when a derivative is zero.
        row = []
        # loop over groups of collocation points which corresponds to different derivative orders
        # for d in range(len(self.collocation_points)):
        for d in self.collocation_points.keys():
            # loop over each collocation point for each derivative
            for c in self.collocation_points[d]:
                # take derivative of each term in the ansatz
                terms = [sympy.diff(term, x_sym, d) for term in self.ansatz.args]
                # evaluate terms at given collocation point
                sub_dict = {"x_sym": c}
                # evaluate terms at given constants (if any)
                if self.sub_dict is not None:
                    sub_dict.update(self.sub_dict)
                row.append([term.subs(sub_dict) for term in terms])
        information_matrix = np.array(row, dtype=np.float64)
        self.information_matrix = information_matrix

    def solve(self, information_matrix=None, rhs=None):
        """
        information_matrix : None, default is None
            This matrix contains the value of variables
            (indeterminates) of the model/ansatz at the collocation
            points.
            If not given then uses the current one.
        rhs : None, default is None
            Flattened rhs dictionary. If not given then uses the current one.
        """
        if information_matrix is None:
            information_matrix = self.information_matrix
        if rhs is None:
            rhs = self.rhs_1d
        self.coeffs = np.linalg.solve(information_matrix, rhs)

    def get_basis(self, X: npt.NDArray, dtype=object):
        """
        Turn this into a property so that it only gets calculated
        once/when it needs to.

        X : npt.NDArray
            TODO
        dtype : object
            used to be object because in sympy when we have a constant
            term such as x_sym**0 this gets simplified to just '1'.
            This doesn't get broadcast when you pass an array but
            seems to work with dtype=object
        """
        basis = np.array([t(X) for t in self.terms_fn], dtype=dtype)
        return basis

    def predict(self, X: npt.NDArray, dtype=np.float64) -> npt.NDArray:
        # turn basis into a property that only gets
        # recalculated when the `x`s change.
        basis = self.get_basis(X)

        return np.dot(self.coeffs, basis).astype(dtype)
