# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     Scipion Team
# *
# * National Center of Biotechnology, CSIC, Spain
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
from enum import Enum
from pyworkflow.protocol import BooleanParam, FloatParam, EnumParam, \
    PointerParam, IntParam, GE
from reliontomo import Plugin
from reliontomo.constants import OUT_PARTICLES_STAR, COORD_X, COORD_Y, COORD_Z, SHIFTX_ANGST, SHIFTY_ANGST, \
    SHIFTZ_ANGST, ROT, TILT, PSI
from reliontomo.objects import RelionSetOfPseudoSubtomograms
from reliontomo.protocols.protocol_base_relion import ProtRelionTomoBase, IS_RELION_50
from reliontomo.utils import genEnumParamDict

# Operation labels and values
NO_OPERATION = 'No operation'
OP_ADDITION = 'Add'
OP_MULTIPLICATION = 'Multiply'
OP_SET_TO = 'Set to'
OPERATION_LABELS = [NO_OPERATION, OP_ADDITION, OP_MULTIPLICATION, OP_SET_TO]

# Labels to which apply the operation
COORDINATES = 'coordinates'
SHIFTS = 'shifts'
ANGLES = 'angles'
LABELS_TO_OPERATE_WITH = [COORDINATES, SHIFTS, ANGLES]


class outputObjects(Enum):
    relionParticles = RelionSetOfPseudoSubtomograms


class ProtRelionEditParticlesStar(ProtRelionTomoBase):
    """Operate on the particles star file"""

    _label = 'Apply operation to Relion particles'
    _possibleOutputs = outputObjects
    operationDict = genEnumParamDict(OPERATION_LABELS)
    labelsDict = genEnumParamDict(LABELS_TO_OPERATE_WITH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):
        super()._defineCommonInputParams(form)
        form.addSection(label='Center')
        form.addParam('doRecenter', BooleanParam,
                      label='Perform centering of particles',
                      default=False,
                      help='Perform centering of particles according to a position in the reference.')
        group = form.addGroup('Shift center', condition='doRecenter')
        group.addParam('averageSubTomogram',
                       PointerParam,
                       pointerClass='AverageSubTomogram',
                       label='Average of subtomogram (optional)',
                       allowsNull=True)
        group.addParam('refMask',
                       PointerParam,
                       pointerClass='VolumeMask',
                       label='Reference mask (optional)',
                       allowsNull=True)
        group.addParam('shiftX', FloatParam,
                       label='X (pix.)',
                       default=0,
                       help='X-coordinate in the reference to center particles on (in pix)')
        group.addParam('shiftY', FloatParam,
                       label='Y (pix.)',
                       default=0,
                       help='Y-coordinate in the reference to center particles on (in pix)')
        group.addParam('shiftZ', FloatParam,
                       label='Z (pix.)',
                       default=0,
                       help='Z-coordinate in the reference to center particles on (in pix)')
        # Section 'Remove duplicates' was added in Relion 5
        if IS_RELION_50:
            form.addSection('Remove duplicates')
            form.addParam('doRemoveDuplicates', BooleanParam,
                          default=False,
                          label='Remove duplicates?',
                          help='If set to Yes, duplicated particles that are within a given distance are removed '
                               'leaving only one. Duplicated particles are sometimes generated when particles drift '
                               'into the same position during alignment. They inflate and invalidate gold-standard '
                               'FSC calculation.')
            form.addParam('minDistPartRemoval', IntParam,
                          default=30,
                          label='Minimum inter-particle distance (Å)',
                          condition='doRemoveDuplicates',
                          validators=[GE(0)],
                          help='Particles within this distance are removed leaving only one.')
        else:
            # This section is rarely used and makes nonsense in Relion 5 as there is not a explicit field for the
            # coordinates
            form.addSection(label='Operate')
            form.addParam('chosenOperation', EnumParam,
                          choices=list(self.operationDict.keys()),
                          default=self.operationDict[NO_OPERATION],
                          label='Choose operation')
            form.addParam('opValue', FloatParam,
                          condition='chosenOperation != %i' % self.operationDict[NO_OPERATION],
                          default=1,
                          label='Value to operate the selected labels')
            group = form.addGroup('Operation', condition='chosenOperation > 0')
            group.addParam('operateWith', EnumParam,
                           choices=list(self.labelsDict.keys()),
                           default=self.labelsDict[COORDINATES],
                           label='Operate with')
            group.addParam('label1x', BooleanParam,
                           label='X (pix.)',
                           condition='operateWith == %s' % self.labelsDict[COORDINATES],
                           default=False)
            group.addParam('label2y', BooleanParam,
                           label='Y (pix.)',
                           condition='operateWith == %s' % self.labelsDict[COORDINATES],
                           default=False)
            group.addParam('label3z', BooleanParam,
                           label='Z (pix.)',
                           condition='operateWith == %s' % self.labelsDict[COORDINATES],
                           default=False)
            group.addParam('label1sx', BooleanParam,
                           label='Shift X (pix.)',
                           condition='operateWith == %s' % self.labelsDict[SHIFTS],
                           default=False)
            group.addParam('label2sy', BooleanParam,
                           label='Shift Y (pix.)',
                           condition='operateWith == %s' % self.labelsDict[SHIFTS],
                           default=False)
            group.addParam('label3sz', BooleanParam,
                           label='Shift Z (pix.)',
                           condition='operateWith == %s' % self.labelsDict[SHIFTS],
                           default=False)
            group.addParam('label1rot', BooleanParam,
                           label='Rot (deg.)',
                           condition='operateWith == %s' % self.labelsDict[ANGLES],
                           default=False)
            group.addParam('label2tilt', BooleanParam,
                           label='Tilt (deg.)',
                           condition='operateWith == %s' % self.labelsDict[ANGLES],
                           default=False)
            group.addParam('label3psi', BooleanParam,
                           label='Psi (deg.)',
                           condition='operateWith == %s' % self.labelsDict[ANGLES],
                           default=False)

    # -------------------------- INSERT steps functions -----------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.convertInputStep, needsGPU=False)
        self._insertFunctionStep(self.operateStep, needsGPU=False)
        self._insertFunctionStep(self.createOutputStep, needsGPU=False)

    def convertInputStep(self):
        are2dParticles = getattr(self.inReParticles.get(), RelionSetOfPseudoSubtomograms.ARE_2D_PARTICLES, False)
        self.genInStarFile(are2dParticles=are2dParticles)

    def operateStep(self):
        program = 'relion_star_handler'
        if IS_RELION_50:
            # Remove duplicates and re-center particles needs to be executed separately, being the second call to the
            # program required to be fed with the ourpur star of the first
            doRemDuplicates = self.doRemoveDuplicates.get()
            doRecenter = self.doRecenter.get()
            if doRemDuplicates and doRecenter:
                Plugin.runRelionTomo(self, program, self._genRemDuplicatesCmd())
                outParticles = self._getExtraPath(OUT_PARTICLES_STAR)
                cmd = '--i %s ' % outParticles
                cmd += '--o %s ' % outParticles
                cmd += self._genRecenterCmd()
                Plugin.runRelionTomo(self, program, cmd)
            else:
                if doRemDuplicates:
                    Plugin.runRelionTomo(self, program, self._genRemDuplicatesCmd())
                if doRecenter:
                    Plugin.runRelionTomo(self, program, self._genRecenterCmdWithIO())
        else:
            Plugin.runRelionTomo(self, program, self._getOperateCommand())

    def createOutputStep(self):
        psubtomoSet = self.genRelionParticles()
        self._defineOutputs(**{outputObjects.relionParticles.name: psubtomoSet})
        self._defineSourceRelation(self.inReParticles, psubtomoSet)

    # -------------------------- INFO functions -------------------------------
    def _validate(self):
        valMsg = []
        if IS_RELION_50:
            if not self.doRecenter.get() and not self.doRemoveDuplicates.get():
                valMsg.append('No re-centering nor duplicate removal operation was chosen.')
        else:
            if not self.doRecenter.get() and self.chosenOperation.get() == self.operationDict[NO_OPERATION]:
                valMsg.append('No re-centering or operation was chosen.')
        return valMsg

    # --------------------------- UTILS functions -----------------------------
    def _genIOCmd(self):
        cmd = '--i %s ' % self.getOutStarFileName()
        cmd += '--o %s ' % self._getExtraPath(OUT_PARTICLES_STAR)
        return cmd

    def _genRemDuplicatesCmd(self):
        cmd = self._genIOCmd()
        cmd += '--remove_duplicates %i ' % self.minDistPartRemoval.get()
        return cmd

    def _genRecenterCmd(self):
        cmd = '--center '
        if self.shiftX.get() != 0:
            cmd += '--center_X %.2f ' % self.shiftX.get()
        if self.shiftY.get() != 0:
            cmd += '--center_Y %.2f ' % self.shiftY.get()
        if self.shiftZ.get() != 0:
            cmd += '--center_Z %.2f ' % self.shiftZ.get()
        return cmd

    def _genRecenterCmdWithIO(self):
        cmd = self._genIOCmd()
        cmd += self._genRecenterCmd()
        return cmd

    def _getOperateCommand(self):
        cmd = self._genIOCmd()
        # Re-center particles
        if self.doRecenter.get():
            cmd += self._genRecenterCmd()

        # Operate particles - removed by Jorge in the protocol version for Relion 5 as it is rarely used and may
        # be problematic as some of the fields involved are now defined in a different way, such as the coordinates
        if self.chosenOperation.get() != self.operationDict[NO_OPERATION]:
            opValue = self.opValue.get()
            chosenOp = self.chosenOperation.get()
            # Chosen operation
            if chosenOp == self.operationDict[OP_ADDITION]:
                cmd += '--add_to %.2f ' % opValue
            elif chosenOp == self.operationDict[OP_MULTIPLICATION]:
                cmd += '--multiply_by %.2f ' % opValue
            else:
                cmd += '--set_to %.2f ' % opValue
            # Chosen values
            cmd += self._genOperateCmd()
        return cmd

    def _genOperateCmd(self):
        """Three are the maximum number of labels able to be edited at once. Relion offers 3 arguments to add them
        to the generated command: --operate, --operate2, --operate3."""
        operateWith = self.operateWith.get()
        if operateWith == self.labelsDict[COORDINATES]:
            label1, label2, label3 = COORD_X, COORD_Y, COORD_Z
            edit1, edit2, edit3 = self.label1x.get(), self.label2y.get(), self.label3z.get()
        elif operateWith == self.labelsDict[ANGLES]:
            label1, label2, label3 = ROT, TILT, PSI
            edit1, edit2, edit3 = self.label1rot.get(), self.label2tilt.get(), self.label3psi.get()
        else:
            label1, label2, label3 = SHIFTX_ANGST, SHIFTY_ANGST, SHIFTZ_ANGST
            edit1, edit2, edit3 = self.label1sx.get(), self.label2sy.get(), self.label3sz.get()

        operateCmd = ''
        labelList = [label1, label2, label3]
        editList = [edit1, edit2, edit3]
        counter = 1
        for label, editVal in zip(labelList, editList):
            if editVal:
                if counter == 1:
                    operateCmd += '--operate %s ' % label
                else:
                    operateCmd += '--operate%i %s ' % (counter, label)
                counter += 1

        return operateCmd

    def getAverageSubTomogram(self):
        return self.averageSubTomogram.get()

    def getMask3D(self):
        return self.refMask.get()
