FROM continuumio/miniconda3:latest

LABEL maintainer="Seignovert"

# Install shared libs and rsync
RUN apt-get -qq update && \
    apt-get install -y rsync \
    libglu1 \
    libgl1

# Set ENV variables
ENV HOME=/usgs
ENV ISISROOT=$HOME/isis3 ISIS3DATA=$HOME/data
ENV PATH=$PATH:$ISISROOT/bin

# Create user and home
RUN useradd --create-home --home-dir $HOME --shell /bin/bash usgs

# Copy all files to usgs/
COPY . $HOME/
WORKDIR $HOME


# Sync ISIS with conda
RUN conda config --add channels conda-forge && \
    conda config --add channels usgs-astrogeology && \
    conda create -y --prefix ${ISISROOT} && \
    conda install -y --prefix ${ISISROOT} isis3

# Sync partial `base` data
RUN rsync -azv --delete --partial \
    --exclude='dems/*.cub' \
    --exclude='testData' \
    isisdist.astrogeology.usgs.gov::isis3data/data/base $ISIS3DATA

# Remove docs
RUN rm -rf $ISISROOT/doc $ISISROOT/docs

# Add Isis User Preferences
RUN mkdir -p $HOME/.Isis && echo "Group = UserInterface\n\
  ProgressBar      = Off\n\
  HistoryRecording = Off\n\
EndGroup\n\
\n\
Group = SessionLog\n\
  TerminalOutput = Off\n\
  FileOutput     = Off\n\
EndGroup" > $HOME/.Isis/IsisPreferences

WORKDIR $HOME
RUN pip install -r requirements.txt

WORKDIR CaptionWriter
CMD python ISSS.py










