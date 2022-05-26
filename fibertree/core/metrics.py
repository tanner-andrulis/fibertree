#cython: language_level=3
class Metrics:
    """A globally available class for tracking metrics.

    The Metrics class provides an interface for collecting metrics from the
    execution of an HFA kernel. All methods are class-level so that the metrics
    can be updated and read from anywhere.

    Attributes
    ----------

    The Metrics class has a set of attributes that can be set and accessed.
    These include:

    - A **collecting** boolean, which specifies whether or not data collection
      is in progress.

    - A **metrics** list, which contains dictionaries associated with the metrics
      collected by the program.


    Constructor
    ----------

    There is no reason to ever create an instance of the Metrics class

    """
    # Create a class instance variable for the metrics collection
    collecting = False
    iteration = None
    last_iter = None
    line_order = None
    loop_order = None
    metrics = None
    num_cached_uses = 1000
    point = None
    prefix = None
    trace = {}

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def addUse(cls, rank, coord):
        """Add a use of all tensors at the given rank and coord

        Parameters
        ----------

        rank: str
            The name of the rank

        coord: int
            The coordinate at this rank

        Returns
        -------

        None

        """
        # Update the point
        i = cls.line_order[rank]
        cls.point[i] = coord

        # Make sure we are tracking this rank
        if rank not in cls.trace.keys():
            return

        # Make sure that the most updated version of the point is being traced
        # (for example, in cases where there are multiple iterators per rank)
        if cls.iteration[:(i + 1)] == cls.last_iter[rank]:
            cls.removeUse(rank)

        cls.last_iter[rank] = cls.iteration[:(i + 1)]


        # Add the trace
        iteration = ",".join(str(j) for j in cls.iteration[:(i + 1)])
        point = ",".join(str(j) for j in cls.point[:(i + 1)])
        cls.trace[rank].append(iteration + "," + point + "\n")

        # If we are at the limit of the number of cached uses, write the data
        # to disk
        if len(cls.trace[rank]) == cls.num_cached_uses + 1:
            cls._writeTrace(rank, cls.trace[rank][:-1])
            cls.trace[rank] = [cls.trace[rank][-1]]

    @classmethod
    def beginCollect(cls, prefix, loop_order):
        """Begin metrics collection

        Start collecting metrics during future HFA program execution.

        Parameters
        ----------

        prefix: str
            The prefix to the files that will store the reuse statistics

        loop_order: [str]
            The order of ranks in the loop order

        Returns
        -------

        None

        """
        cls.collecting = True
        cls.iteration = [0] * len(loop_order)
        cls.last_iter = {}
        cls.line_order = {r: i for i, r in enumerate(loop_order)}
        cls.loop_order = loop_order
        cls.metrics = {}
        cls.point = [0] * len(loop_order)
        cls.prefix = prefix
        cls.trace = {}


    @classmethod
    def clrIter(cls, line):
        """Clear the given line's iteration counter

        Parameters
        ----------

        line: string
            The name of the line number this metric is associated with

        Returns
        -------

        None

        NDN: Test

        """
        if line not in cls.line_order.keys():
            return

        cls.iteration[cls.line_order[line]] = 0


    @classmethod
    def dump(cls):
        """Get the most-recently collected set of metrics

        Return the dictionary containing all metrics collected since the most
        recent `Metrics.beginCollect()`

        Parameters
        ----------

        None

        Returns
        -------

        metrics: a dictionary
            The dictionary of metrics collected

        """
        return cls.metrics

    @classmethod
    def endCollect(cls):
        """End metrics collection

        Stop collecting metrics during future HFA program execution.

        Parameters
        ----------

        None

        Returns
        -------

        None

        """
        # Save the trace of uses
        for rank in cls.trace.keys():
            cls._writeTrace(rank, cls.trace[rank])

        # Clear all info
        cls.collecting = False
        cls.iteration = None
        cls.last_iter = None
        cls.line_order = None
        cls.loop_order = None
        cls.num_cached_uses = 1000
        cls.point = None
        cls.prefix = None
        cls.trace = {}

    @classmethod
    def getIter(cls):
        """Get the inner loop iteration number

        Parameters
        ----------

        None

        Returns
        -------

        None

        """
        return tuple(cls.iteration)


    @classmethod
    def incCount(cls, line, metric, inc):
        """Increment a count metric during collection

        Increment the given count metric associated with the given line of
        code by the specified amount. If the line or metric is not already
        being tracked, they are first added to the dictionary of metrics.

        Parameters
        ----------

        line: string
            The name of the line number this metric is associated with

        metric: string
            The name of the metric

        inc: int
            The amount to increment the metric by.

        Returns
        -------

        None

        """

        line = line.strip()

        if line not in cls.metrics:
            cls.metrics[line] = {}

        if metric not in cls.metrics[line]:
            cls.metrics[line][metric] = 0

        cls.metrics[line][metric] += inc


    @classmethod
    def incIter(cls, line):
        """Increment the given line's iteration number by one

        Parameters
        ----------

        line: string
            The name of the line number this metric is associated with

        Returns
        -------

        None

        """
        if line not in cls.line_order.keys():
            return

        cls.iteration[cls.line_order[line]] += 1

    @classmethod
    def isCollecting(cls):
        """Returns True during metrics collection

        Returns True if metrics are being collected, and false if they are not.

        Parameters
        ----------

        None

        Returns
        -------

        None

        """
        return cls.collecting

    @classmethod
    def removeUse(cls, rank):
        """
        Remove the last use of a rank

        Note: necessary in cases like intersection where a fiber coordinate may
        be accessed earlier, but its payload was never accessed

        Parameters
        ----------

        rank: str
            The rank whose use to remove

        Returns
        -------

        None

        """
        if rank in cls.trace.keys():
            cls.last_iter[rank] = None
            cls.trace[rank].pop()

    @classmethod
    def setNumCachedUses(cls, num_cached_uses):
        """Set the number of uses that are saved to memory before the trace is
        written to disk per rank

        Parameters
        ----------

        num_cached_uses: int
            Number of uses to cache

        Returns
        -------

        None

        """
        assert num_cached_uses > 1

        cls.num_cached_uses = num_cached_uses

    @classmethod
    def traceRank(cls, rank):
        """Set a rank to trace

        Note must be called after Metrics.beginCollect()

        Parameters
        ----------

        rank: str
            The rank to collect the trace of

        Returns
        -------

        None

        """
        assert rank in cls.line_order.keys()

        end = cls.line_order[rank] + 1

        pos = ",".join(r + "_pos" for r in cls.loop_order[:end])
        coord = ",".join(r for r in cls.loop_order[:end])

        with open(cls.prefix + "-" + rank + ".csv", "w") as f:
            f.write("")

        cls.last_iter[rank] = None
        cls.trace[rank] = [pos + "," + coord + "\n"]

    @classmethod
    def _writeTrace(cls, rank, trace):
        """Write the trace to the file

        Parameters
        ----------

        rank: str
            The rank whose trace to write

        trace: List[str]
            The trace of uses

        Returns
        -------

        None

        """
        with open(cls.prefix + "-" + rank + ".csv", "a") as f:
           for use in trace:
                f.write(use)
